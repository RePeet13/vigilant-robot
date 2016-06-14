import argparse, math

#####
# Here be secrets
#####
# If you'd like to substitute your own secret function(s), all you have 
# to do is define a new function in the Secret class, and change the 
# return of the secret() to that function.
#####
class Secret:
    'Class to abstract a secret function, and allow it to be swapped in and out.'

    def secret(self, num):
        return num
        # return simpleSecret(num);

    def simpleSecret(self, num):
        return 2*num

    def weirdSecret(self, num):
        num = math.factorial(num)+5
        num = num/6
        return num


# This function returns a list of all the primes under the passed in num
# via the simple Sieve of Eratosthenes (with a few skipped steps)
# ( https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes ) which is an 
# efficient way to find smaller primes.
def subPrimes(num):
    candidates = [True] * num

    # Iterate through the list skipping the odds, and only considering 
    # up to the square root of the passed in number, as above that 
    # all the multiples are guaranteed to be taken care of already.
    for i in xrange(3,int(num**0.5)+1,2):

        # If the candidate has not been ruled out yet, rule out it's 
        # multiples later in the candidate list
        if candidates[i]:

            # Start at i^2 because all multiples below that will have 
            # necessarily been ruled out already, slice through the 
            # end of the list, and step by 2*i because you start on an 
            # odd (odd*odd=odd), and can safely skip the multiples of 
            # even numbers (eg. 7*8 has to be even because it could be 
            # rewritten as 7*4*2, or n*2, which is always even)
            candidates[i*i::2*i] = [False] * ((num-i*i-1)/(2*i)+1)

    # Prepend only even prime: two, to the list
    #
    # Start list comprehension at 3, and skip odds, bringing to the final 
    # list only the numbers that were not sieved out
    primes = [2] + [x for x in xrange(3,num,2) if candidates[x]]

    # Uncomment to see all the primes below the passed in number
    # print 'Primes below ' + str(num) + ' are:\n\t' + str(primes)

    return primes


### ------------------------ ###
### Test Functions/Helpers   ###
### ------------------------ ###
def tests(secret):

    ### ------------------------ ###
    ### Prime Generation Test    ###
    ### ------------------------ ###
    # First check that the primes generator is working properly 
    # by running it and verifying vs. primes from generators on the web.
    primesGold=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
    61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
    229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
    313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
    409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
    499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
    691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
    907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997)
    
    failed = False
    message = ''

    myPrimes = subPrimes(1000)

    if len(primesGold) != len(myPrimes):
        failed = True
        message = 'Length of prime arrays are different'
    else:
        for i in xrange(len(primesGold)):
            if primesGold[i] != myPrimes[i]:
                failed = True
                message = 'primesGold['+str(i)+'] ('+str(primesGold[i])+') did not match myPrimes['+str(i)+'] ('+str(myPrimes[i])+')'
                break;

    reportTestResults('Prime Generation', failed, message)


    ### ------------------------ ###
    ### Test Name
    ### ------------------------ ###




### Have a common format for test results so its legible
def reportTestResults(testName, failed, message=''):
    p = testName + ' Test : ' + ('Failed' if failed else 'Passed')

    # If it failed and had a message, go ahead and print that too
    if failed and message:
        p = p + '\n\t' + message + '\n'
    print p



### Respond to call from command line ###
if __name__ == "__main__":
    ### Arg Parsing ###
    parser = argparse.ArgumentParser()
    parser.add_argument('number', help='All primes tested with the secret function will be under this value')
    parser.add_argument('-t', '--test', help='Add this flag to run the tests', action='store_true')
    args = parser.parse_args()

    # Instantiate the secret class
    s = Secret()

    if args.test:
        tests(s)

