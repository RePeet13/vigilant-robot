import argparse, math, sys

### ------------------------ ###
### Here be secrets          ###
### ------------------------ ###
# If you'd like to substitute your own secret function(s), all you have 
# to do is define a new function in the Secret class, and change the 
# return of the secret() to that function.
#####
class Secret:
    'Class to abstract a secret function, and allow it to be swapped in and out.'

    def __init__(self, functionName='secret'):
        self.fn=functionName

    def compute(self, num):
        return {
            'secret' : secret(num),
            'superSimpleSecret': superSimpleSecret(num),
            'simpleSecret' : simpleSecret(num),
            'weirdSecret' : weirdSecret(num),
            'nonAdditiveSecret' : nonAdditiveSecret(num),
        }.get(self.fn, secret(num))

    # This is the default function that will be called if you don't 
    # pass a different function name, which is mainly used to enable  
    # testing.
    def secret(self, num):
        return superSimpleSecret(num);

    ### ------------------------ ###

    def superSimpleSecret(self, num):
        return num

    def simpleSecret(self, num):
        return 2*num

    def weirdSecret(self, num):
        num = math.factorial(num)+5
        num = num//6
        return num

    def nonAdditiveSecret(self, num):
        return num**2

    def changeFunction(self, functionName):
        self.fn=functionName


def isSecretAdditive(secret, num):
    # Input validation
    num = int(num)
    # TODO have except here to catch and set nanMessage

    # Verify large prime generation
    if num > 1000000:

        # If very large fail fast (this could be disabled with a 
        # with a commandline flag like: 'No warranty mode')
        if num > 1000000000:
            return largePrimeMessage

        a = input('Continue with generation of large primes? It could take a while... (y/n): ')
        
        if a.lower() is 'y' or a.lower() is 'yes':
            return 'Stop requested by user'

        

    # Generate Primes
    primes = subPrimes(num)

    return "Still working on method"


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
### Standard Messages        ###
### ------------------------ ###
successMessage = 'Success! The secret function is additive for all primes lower than value given\n\tAdditive means: secret( x+y ) = secret( x ) + secret( y )'
failedMessage = 'Failed! The secret function is not additive for all primes lower than the value given'
nanMessage = 'Failed! Input given is not a number.'
largePrimeMessage = 'Program was stopped because primes would be very large'


### ------------------------ ###
### Test Functions/Helpers   ###
### ------------------------ ###
def tests(secret):


    ### ------------------------ ###
    ### Input Validation Tests   ###
    ### ------------------------ ###
    # Check that input validations are working properly
    failed = False
    message = ''

    # Test number in string parses correctly
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, '5')
        if m is not successMessage:
            failed = True
            message = 'Failed to parse number in a string'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])
    
    reportTestResults('String Number Input', failed, message)


    failed = False
    message = ''

    # Test string input
    # This case is the same as 'all letter string' and 'empty string'
    # Don't need to test for NoneType, because the argument parser 
    # enforces having a value.
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, '5foo')
        if m is not nanMessage:
            failed = True
            message = 'Failed to recognize string was not a number'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])
    
    reportTestResults('String Input', failed, message)


    ### ------------------------ ###
    ### Overlarge Prime Test     ###
    ### ------------------------ ###
    failed = False
    message = ''

    # Test one more than limit (could extract this limit to be a global var)
    try:
        m = isSecretAdditive(secret, 1000000001)
        if m is not largePrimeMessage:
            failed = True
            message = 'Failed to break when given a barely overlarge number for primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Overlarge Prime', failed, message)
    

    ### ------------------------ ###
    ### Way Large Prime Test     ###
    ### ------------------------ ###
    failed = False
    message = ''

    # Test random lots more than limit number
    try:
        m = isSecretAdditive(secret, 35206089431)
        if m is not largePrimeMessage:
            failed = True
            message = 'Failed to break when given a very overlarge number for primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Way large Prime', failed, message)


    ### ------------------------ ###
    ### Prime Generation Test    ###
    ### ------------------------ ###
    # Check that the primes generator is working properly 
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

    try:
        myPrimes = subPrimes(1000)

        if len(primesGold) != len(myPrimes):
            failed = True
            message = 'Length of prime arrays are different'
        else:
            for i in xrange(len(primesGold)):
                if primesGold[i] != myPrimes[i]:
                    failed = True
                    message = 'primesGold[{id}] ({pg}) did not match myPrimes[{id}] ({mp})'\
                        .format(id=i, pg=str(primesGold[i]), mp=str(myPrimes[i]))
                    break;
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Prime Generation', failed, message)


    ### ------------------------ ###
    ### Simple Additive 1 Test   ###
    ### ------------------------ ###
    failed = False
    message = ''

    # Test with a super simple secret that is definitely additive
    # (Just returns the input)
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, 20)
        if m is not successMessage:
            failed = True
            message = 'Failed to identify super simple secret as additive'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Simple Additive 1', failed, message)


    ### ------------------------ ###
    ### Simple Additive 2 Test   ###
    ### ------------------------ ###
    failed = False
    message = ''

    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, 1000)
        if m is not successMessage:
            failed = True
            message = 'Failed to identify super simple secret as additive for larger set of primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Simple Additive 2', failed, message)


    ### ------------------------ ###
    ### Non Additive 1 Test      ###
    ### ------------------------ ###
    failed = False
    message = ''

    # Test with a super simple secret that is definitely additive
    # (Just returns the input)
    try:
        secret.changeFunction('nonAdditiveSecret')
        m = isSecretAdditive(secret, 20)
        if m is not failedMessage:
            failed = True
            message = 'Failed to identify secret as non additive'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Non Additive 1', failed, message)


    ### ------------------------ ###
    ### Non Additive 2 Test      ###
    ### ------------------------ ###
    failed = False
    message = ''

    try:
        secret.changeFunction('nonAdditiveSecret')
        m = isSecretAdditive(secret, 1000)
        if m is not failedMessage:
            failed = True
            message = 'Failed to identify secret as non additive for larger set of primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults('Non Additive 2', failed, message)


### Have a common format for test results so its legible
def reportTestResults(testName, failed, message=''):
    p = testName + ' Test : ' + ('Failed' if failed else 'Passed')

    # If it failed and had a message, go ahead and print that too
    if failed and message:
        p = p + '\n\t' + message + '\n'
    print p


### Respond to call from command line ###
if __name__ == '__main__':
    ### Arg Parsing ###
    parser = argparse.ArgumentParser()
    parser.add_argument('number', help='All primes tested with the secret function will be under this value')
    parser.add_argument('-t', '--test', help='Add this flag to run the tests', action='store_true')
    args = parser.parse_args()
    # print str(args)

    # Instantiate the secret class
    s = Secret()

    if args.test:
        tests(s)

    m = isSecretAdditive(s, args.number)
    if not args.test:
        print str(m)
