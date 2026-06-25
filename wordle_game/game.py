import random
import subprocess
from dataclasses import dataclass

import pygame

from wordle_game.dictionary import wordle_dictionary
from wordle_game.paths import PROJECT_ROOT, SOLVER_BINARY, SOLVER_SOURCE, ensure_runtime_dirs
from wordle_game.ui.animations import Animations
from wordle_game.ui.colors import reset_colors
from wordle_game.ui.interactor import clear_data, get_word, outcome, push_exit
from wordle_game.ui.interface import GameConfig
from wordle_game.ui.letters import Letters
from wordle_game.ui.tiles import Tiles


@dataclass
class GameState:
      configs: GameConfig
      animations: Animations
      tiles: Tiles
      letters: Letters


def normalize_word(word):
      if word is None:
            return random.choice(wordle_dictionary)

      word = word.strip().upper()
      if len(word) != 5:
            raise ValueError("The target word must contain exactly 5 letters.")
      if word not in wordle_dictionary:
            raise ValueError(f"{word} is not in the configured Wordle dictionary.")
      return word


def create_game_state(uses_solver=False):
      ensure_runtime_dirs()
      reset_colors()
      pygame.init()

      animations = Animations()
      animations.turn_on()

      tiles = Tiles(5, 6)
      letters = Letters(tiles.coord, 5, 6)
      configs = GameConfig(uses_solver=uses_solver)
      return GameState(configs=configs, animations=animations, tiles=tiles, letters=letters)


def draw_state(state, score, is_running):
      state.configs.screen_init_(score, is_running)
      state.tiles.draw_table(state.configs.screen)
      state.letters.draw(state.configs.screen, state.configs.font)
      state.configs.update_screen()


def wait_on_finished_game(state, score):
      while True:
            state.configs.event_handle_solver()
            draw_state(state, score, False)


def wait_before_reset(state, score, seconds):
      end_at = pygame.time.get_ticks() + int(seconds * 1000)
      while pygame.time.get_ticks() < end_at:
            state.configs.event_handle_solver()
            draw_state(state, score, False)


def play_manual(target_word=None):
      wordle = normalize_word(target_word)
      state = create_game_state(uses_solver=False)
      run, score = True, 0
      last_invalid_guess = 0

      while run:
            state.configs.screen_init_(score, run)
            state.letters.permute()
            state.tiles.draw_table(state.configs.screen)
            state.letters.draw(state.configs.screen, state.configs.font)

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit

                  if event.type != pygame.KEYDOWN:
                        continue

                  if event.key == pygame.K_BACKSPACE:
                        state.letters.delete_letter()
                        continue

                  if event.key == pygame.K_RETURN:
                        now = pygame.time.get_ticks()
                        guess = "".join(state.letters.str[state.letters.y])

                        if guess in wordle_dictionary:
                              score += 1
                              run = outcome(wordle, state.letters.str[state.letters.y])
                              state.animations.outcome_animation(state.configs, state.tiles, state.letters, score)
                              state.letters.enter_guess()
                              continue

                        if now - last_invalid_guess >= 300:
                              state.animations.worng_animation(state.configs, state.tiles, state.letters, score)
                              last_invalid_guess = pygame.time.get_ticks()
                        continue

                  key_pressed = event.unicode.upper()
                  if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                        state.animations.insert_animation(state.configs, state.tiles, state.letters, score)
                        state.letters.insert_letter(key_pressed)

            state.configs.update_screen()

      wait_on_finished_game(state, score)


def ensure_solver_built():
      ensure_runtime_dirs()
      if SOLVER_BINARY.exists() and SOLVER_BINARY.stat().st_mtime >= SOLVER_SOURCE.stat().st_mtime:
            return

      compile_cmd = ["g++", str(SOLVER_SOURCE), "-O2", "-std=c++17", "-o", str(SOLVER_BINARY)]
      try:
            subprocess.run(compile_cmd, cwd=PROJECT_ROOT, check=True)
      except FileNotFoundError as exc:
            raise RuntimeError("g++ is required to build the C++ solver.") from exc
      except subprocess.CalledProcessError as exc:
            raise RuntimeError("The C++ solver failed to compile.") from exc


def start_solver_process():
      ensure_solver_built()
      clear_data()
      return subprocess.Popen([str(SOLVER_BINARY)], cwd=PROJECT_ROOT)


def finish_solver_process(process):
      if process.poll() is not None:
            return

      push_exit()
      try:
            process.wait(timeout=2)
      except subprocess.TimeoutExpired:
            process.terminate()


def run_solver_game(target_word=None, wait_when_done=True, reset_delay=1.5):
      wordle = normalize_word(target_word)
      state = create_game_state(uses_solver=True)
      process = start_solver_process()
      run, score = True, 0

      try:
            while run:
                  state.configs.event_handle_solver()
                  state.configs.screen_init_(score, run)

                  state.letters.permute()
                  state.tiles.draw_table(state.configs.screen)
                  state.letters.draw(state.configs.screen, state.configs.font)

                  guess = get_word()
                  if len(guess) == 5:
                        score += 1
                        for ch in guess:
                              state.animations.insert_animation(state.configs, state.tiles, state.letters, score)
                              state.letters.insert_letter(ch)

                              if state.animations.active:
                                    state.configs.update_screen(60)

                        run = outcome(wordle, state.letters.str[state.letters.y])
                        state.animations.outcome_animation(state.configs, state.tiles, state.letters, score)
                        state.letters.enter_guess()

                  state.configs.update_screen()
      finally:
            finish_solver_process(process)

      if wait_when_done:
            wait_on_finished_game(state, score)
      else:
            wait_before_reset(state, score, reset_delay)

      return score


def run_solver_loop(reset_delay=1.5):
      while True:
            run_solver_game(wait_when_done=False, reset_delay=reset_delay)
