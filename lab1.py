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
            arr = list()
            for index in range(bytes_number):
                arr.append(random.randint(0, 1))
                self.progress_bar(index, bytes_number)
            print("Done!")
            return arr
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            return list()

    def numpy_builtin_rand(self, bytes_number):
        try:
            print("Starting NumPy builtin pseudo-generator...")
            r = rnd.RandomState()
            r.seed(self.seed)
            arr = list()
            for index in range(bytes_number):
                arr.append(r.choice((0, 1)))
                self.progress_bar(index, bytes_number)
            print("\nDone!")
            return arr
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            return list()

    def fibo_lagged_rand(self, bytes_number):
        try:
            r = random.Random()
            r.seed(self.seed)
            print("Please enter lags (a,b) what to use:\n [1]: (17,5)\n [2]: (55,24)\n [3]: (97,33)\n")
            choice = input("Choice: ")
            if choice is "1":
                (lag_a, lag_b) = (17, 5)
            elif choice is "2":
                (lag_a, lag_b) = (55, 24)
            elif choice is "3":
                (lag_a, lag_b) = (97, 33)
            else:
                print("Wrong choice")
                return list()
            print("\nStarting python builtin pseudo-generator for initial sequence...")
            arr = [r.uniform(0, 1) for i in range(lag_a + 1)]
            print("\nDone!\nStarting fibo pseudo-generator...")
            for index in range(lag_a + 2, bytes_number + 1):
                x_k = arr[index - lag_a] - arr[index - lag_b]
                if x_k < 0:
                    x_k += 1
                arr.append(x_k)
                self.progress_bar(index - lag_a, bytes_number - lag_a)
            print("\nDone!\nChanging values from float to binary...")
            for index, x in enumerate(arr):
                self.progress_bar(index, bytes_number)
                if x < 0.5:
                    arr[index] = 0
                else:
                    arr[index] = 1
            print("\nDone!")
            return arr
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            return list()

    def pm_rand_round(self, last_value):
        IA = 16807
        IM = 2147483647

        next_value = 0

        if last_value is not None or last_value is not 0:
            next_value = IA * last_value % IM
        else:
            raise ValueError("Value should be >= 1")

        return next_value

    def pm_rand(self, bytes_number):
        try:
            arr = list()
            print("\nStarting parka-miller's pseudo-generator...")
            for index in range(bytes_number):
                if index is 0:
                    arr.append(self.pm_rand_round(self.seed))
                arr.append(self.pm_rand_round(arr[index - 1]))
                self.progress_bar(index, bytes_number)
            print("\nDone!\nStarting convert values from integer to binary...")
            bin_arr = list()
            a = (2 ** 31 - 1) // 2
            for index, el in enumerate(arr):
                if el < a + 1:
                    bin_arr.append(0)
                elif el >= a:
                    bin_arr.append(1)
            return bin_arr
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            return list()

    def write_to_file(self, arr):
        print("Writing to file \"%s\"" % self.output_filename)
        with open(self.output_filename, 'w+') as f:
            f.write(''.join([str(x) for x in arr]))
            f.close()
        print("Done!")
