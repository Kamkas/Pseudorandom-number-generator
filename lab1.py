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
        print("Starting python builtin pseudo-generator...")
        random.seed(self.seed, version=2)
        arr = list()
        for index in range(bytes_number):
            arr.append(random.randint(0, 1))
            self.progress_bar(index, bytes_number)
        print("Done!")
        return arr

    def numpy_builtin_rand(self, bytes_number):
        print("Starting NumPy builtin pseudo-generator...")
        # random.seed(self.seed)
        r = rnd.RandomState()
        r.seed(self.seed)
        arr = list()
        try:
            for index in range(bytes_number):
                arr.append(r.choice((0, 1)))
                self.progress_bar(index, bytes_number)
            print("\nDone!")
            return arr
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            return arr

    def fibo_lagged_rand(self, bytes_number):
        arr = list()
        r = random.Random()
        print("Please enter what (a,b) to use:\n [1] (17,5)\n [2] (55,24)\n [3] (97,33)\n")
        choice = input("Choice: ")
        if choice is "1":
            (a, b) = (17, 5)
        elif choice is "2":
            (a, b) = (55, 24)
        elif choice is "3":
            (a, b) = (97, 33)
        else:
            print("Wrong choice")
            return arr
        if bytes_number >= a:
            print("\nStarting python builtin pseudo-generator...")
            r.seed(self.seed)
            for index in range(a):
                arr.append(r.uniform(0.0, 1.0))
                self.progress_bar(index + 1, a)
            print("\nDone!\nStarting fibo pseudo-generator...")
            for index in range(a + 1, bytes_number, 1):
                self.progress_bar(index - a, bytes_number - a)
                if arr[index - a] >= arr[index - b]:
                    arr.append(arr[index - a] - arr[index - b])
                elif arr[index - a] < arr[index - b]:
                    arr.append(arr[index - a] - arr[index - b])
                else:
                    print("generator error occured!")
                    break
            for index, x in enumerate(arr):
                if x < 0.5:
                    arr[index] = 0
                else:
                    arr[index] = 1
            print("Done!")
            return arr

    def pm_rand(self, bytes_number):
        IA = 7 ** 5
        IM = 2 ** 31 - 1
        AM = 1.0 / IM

        IQ = 12773
        IR = 2836

        MASK = 123456789

        seed = self.seed

        seed ^= MASK
        k = seed / IQ
        seed = IA * (seed - k * IQ) - IR * k
        if seed < 0:
            seed += IM
        ans = AM * seed
        seed ^= MASK
        return ans

    def write_to_file(self, arr):
        print("Writing to file \"%s\"" % self.output_filename)
        with open(self.output_filename, 'w+') as f:
            f.write(''.join([str(x) for x in arr]))
            f.close()
        print("Done!")


if __name__ == '__main__':
    g = Generator(None, None)
    # print(g.python_builtin_rand(5))
    # print(g.numpy_builtin_rand(5))
    print(g.seed)
    g.python_builtin_rand(100000)