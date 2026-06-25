import argparse


def build_parser():
      parser = argparse.ArgumentParser(description="Play Wordle manually or watch the solver play.")
      subparsers = parser.add_subparsers(dest="command", required=True)

      play_parser = subparsers.add_parser("play", help="Play Wordle manually.")
      play_parser.add_argument("--word", help="Use a fixed target word for testing.")

      solve_parser = subparsers.add_parser("solve", help="Let the solver play one Wordle game.")
      solve_parser.add_argument("--word", help="Use a fixed target word for testing.")

      loop_parser = subparsers.add_parser("loop", help="Let the solver play, reset, and repeat forever.")
      loop_parser.add_argument("--reset-delay", type=float, default=1.5, help="Seconds to show the solved board before resetting.")

      return parser


def main(argv=None):
      parser = build_parser()
      args = parser.parse_args(argv)

      if args.command == "play":
            from wordle_game.game import play_manual

            play_manual(args.word)
      elif args.command == "solve":
            from wordle_game.game import run_solver_game

            run_solver_game(args.word)
      elif args.command == "loop":
            from wordle_game.game import run_solver_loop

            run_solver_loop(args.reset_delay)


if __name__ == "__main__":
      main()
