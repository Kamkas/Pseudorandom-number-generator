import random
import sys

from numpy import random as rnd


class Generator:
    def __init__(self, seed, output_filename):
        if not seed:
            self.seed = random.randrange(1, 2 ** 31, 1)
        else:
            self.seed = int(seed)
        self.output_filename = output_filename
        self.bytes_number = 0

    @staticmethod
    def progress_bar(count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()

    def python_builtin_rand(self, bytes_number):
        try:
            print("Starting python builtin pseudo-generator...")
            random.seed(self.seed, version=2)
            for index in range(bytes_number):
                self.progress_bar(index, bytes_number)
                yield str(random.randint(0, 1))
            print("Done!")
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            raise StopIteration

    def numpy_builtin_rand(self, bytes_number):
        try:
            print("Starting NumPy builtin pseudo-generator...")
            r = rnd.RandomState()
            r.seed(self.seed)
            for index in range(bytes_number):
                self.progress_bar(index, bytes_number)
                yield str(r.choice((0, 1)))
            print("\nDone!")
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            raise StopIteration

    def fibo_lagged_rand(self, bytes_number):
        try:
            r = random.Random()
            r.seed(self.seed)
            print("Fibonacci lagged pseudo random generator.\n \
                Please enter lags (a,b) what to use:\n [1]: (17,5)\n [2]: (55,24)\n [3]: (97,33)\n")
            choice = input("Choice: ")
            if choice is "1":
                (lag_a, lag_b) = (17, 5)
            elif choice is "2":
                (lag_a, lag_b) = (55, 24)
            elif choice is "3":
                (lag_a, lag_b) = (97, 33)
            else:
                print("Wrong choice")
                raise StopIteration
            print("\nStarting python builtin pseudo-generator for initial sequence...")
            arr = [r.uniform(0, 1) for i in range(lag_a + 1)]
            print("\nDone!\nStarting fibo pseudo-generator...")
            for index in range(0, bytes_number):
                x_k = arr[len(arr) - lag_a] - arr[len(arr) - lag_b]
                if x_k < 0:
                    x_k += 1
                arr.append(x_k)
                last_value = arr.pop(0)
                self.progress_bar(index, bytes_number)
                if last_value < 0.5:
                    yield '0'
                else:
                    yield '1'
            print("Done!")
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            raise StopIteration

    def pm_rand(self, bytes_number):
        try:
            print("\nStarting park-miller's pseudo-generator...")
            IA = 16807
            IM = 2147483647
            a = (2 ** 31 - 1) // 2
            prev_value = IA * self.seed % IM
            next_value = 0
            for index in range(1, bytes_number + 1):
                next_value = IA * prev_value % IM
                prev_value = next_value
                self.progress_bar(index, bytes_number + 1)
                if next_value < a + 1:
                    yield '0'
                else:
                    yield '1'
            print("Done!")
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            raise StopIteration

    def write_iter_to_file(self, iterator):
        print("Writing to file \"%s\"" % self.output_filename)
        with open(self.output_filename, 'w+') as f:
            for el in iterator:
                f.write(el)
            f.close()
        print("Done!")

if __name__ == '__main__':
    print("Utility for pseudo random generation of N number of ascii \'0\' and \'1\'.\nIf you want to quit utility, press \"Ctrl+C\"\n")
    while True:
        try:
            print(
                """
                Choose mode that would generate pseudo random sequence:\n
                1. Python builtin random generator\n
                2. NumPy builtin random generator\n
                3. Fibonacci lagged random generator\n
                4. Park-Miller random generator\n
                """
            )
            mode = int(input("Enter mode[1..4]: "))
            seed_number = int(input("Enter seed: "))
            bytes_number = int(input("Enter number of random sequence: "))
            filename = input("Enter file name, which random sequence should be written in \
                (file should be nearby in folder or it would be created): ")
            g = Generator(seed_number, filename)
            if mode is 1:
                g.write_iter_to_file(g.python_builtin_rand(bytes_number))
            elif mode is 2:
                g.write_iter_to_file(g.numpy_builtin_rand(bytes_number))
            elif mode is 3:
                g.write_iter_to_file(g.fibo_lagged_rand(bytes_number))
            elif mode is 4:
                g.write_iter_to_file(g.pm_rand(bytes_number))
            else:
                print("\nWrong mode! Try again!\n")
                continue
        except KeyboardInterrupt:
            print("\nQuit utility.Bye!\n")
            break
        except ValueError as e:
            print("\nError occured! {0}\n".format(e.args))