import argparse, inspect, math, os, sys, time
# Import subfolder modules (this is something I do with most of my python projects)
# from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'lib')))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import progressbar as pb

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
            'secret' : self.secret(num),
            'superSimpleSecret': self.superSimpleSecret(num),
            'simpleSecret' : self.simpleSecret(num),
            'weirdSecret' : self.weirdSecret(num),
            'nonAdditiveSecret' : self.nonAdditiveSecret(num),
        }.get(self.fn, self.secret(num))

    # This is the default function that will be called if you don't 
    # pass a different function name, which is mainly used to enable  
    # testing.
    def secret(self, num):
        return self.superSimpleSecret(num);

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

    # Included to allow test class to specify the function to run
    def changeFunction(self, functionName):
        self.fn=functionName


def isSecretAdditive(secret, num):
    # Input validation
    try:
        num = int(math.ceil(float(num)))
    except ValueError:
        return nanMessage

    # No primes exist under 2
    if num <= 2:
        return noPrimesMessage

    # Verify large prime generation
    if num > 1000000:

        # If very large fail fast (this could be disabled with a 
        # with a commandline flag like: 'No warranty mode')
        if num > 1000000000:
            return largePrimeMessage

        a = input('Continue with generation of large primes? It could take a while... (y/n): ')
        
        if a.lower() is 'y' or a.lower() is 'yes':
            return 'Stop requested by user'

    primes = subPrimes(num)

    # Slight optimization to only calculate each combination once by 
    # skipping the transposed lower half triangle of the matrix.
    # The worst case is when the secret is additive, as it will have to go 
    # through all combinations. It seems like generally if it's not 
    # additive it will be should be clear fairly quick. Due to that I've 
    # set the method to fail fast. Therefore Non-additive secrets should run 
    # fairly quick after prime generation. The only exception I can think 
    # of is if the function is non continuous, eg. additive under a point 
    # and not above that point.
    progress = pb.ProgressBar(widgets=[
                ' ', pb.widgets.Percentage(),
                ' ', pb.widgets.Bar(),
                ' ', pb.widgets.Timer(),
                ' ', pb.widgets.AdaptiveETA(), ' '
            ]) # bit of styling to make the bar make more sense
    print 'Checking if function is Additive'
    for i in progress(range(len(primes))):
        for j in range(i,len(primes)):
            if secret.compute(primes[i] + primes[j]) != secret.compute(primes[i]) + secret.compute(primes[j]):
                return failedMessage

    return successMessage


# This function returns a list of all the primes under the passed in num
# via the simple Sieve of Eratosthenes (with a few skipped steps)
# ( https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes ) which is an 
# efficient way to find smaller primes. If large primes were desired, 
# a more efficient algorithm like a Wheel based approach would be used.
def subPrimes(num):
    candidates = [True] * num

    # Iterate through the list skipping the odds, and only considering 
    # up to the square root of the passed in number, as above that 
    # all the multiples are guaranteed to be taken care of already.
    for i in range(3,int(num**0.5)+1,2):

        # If the candidate has not been ruled out yet, rule out it's 
        # multiples later in the candidate list.
        if candidates[i]:

            # Start at i^2 because all multiples below that will have 
            # necessarily been ruled out already, slice through the 
            # end of the list, and step by 2*i because you start on an 
            # odd (odd*odd=odd), and can safely skip the multiples of 
            # even numbers (eg. 7*8 has to be even because it could be 
            # rewritten as 7*4*2, or n*2, which is always even). The right 
            # half just computes the number of multiples being set.
            candidates[i*i::2*i] = [False] * ((num-i*i-1)/(2*i)+1)

    # Prepend only even prime: two, to the list
    #
    # Start list comprehension at 3, and skip odds, bringing to the final 
    # list only the numbers that were not sieved out
    primes = [2] + [x for x in range(3,num,2) if candidates[x]]

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
noPrimesMessage = 'No primes were found below the value given'


### ------------------------ ###
### Test Functions/Helpers   ###
### ------------------------ ###
def tests(secret):

    ### ------------------------ ###
    ### Input Validation Tests   ###
    ### ------------------------ ###
    reportTestStart('Input Validation')
    # Check that input validations are working properly
    failed = False
    message = ''
    start = time.clock()

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
    
    reportTestResults(failed, start, message)


    # Check that input validations are working properly
    failed = False
    message = ''
    start = time.clock()

    # Test float parses correctly
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, 5.0)
        if m is not successMessage:
            failed = True
            message = 'Failed to parse number in a string'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])
    
    reportTestResults(failed, start, message)


    failed = False
    message = ''
    start = time.clock()

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
    
    reportTestResults(failed, start, message)


    failed = False
    message = ''
    start = time.clock()

    # Test low number input
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, 2)
        if m is not noPrimesMessage:
            failed = True
            message = 'Failed to recognize input was too low'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])
    
    reportTestResults(failed, start, message)


    failed = False
    message = ''
    start = time.clock()

    # Test low number input
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, -12)
        if m is not noPrimesMessage:
            failed = True
            message = 'Failed to recognize input was too low'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])
    
    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Overlarge Prime Test     ###
    ### ------------------------ ###
    reportTestStart('Overlarge Prime')
    failed = False
    message = ''
    start = time.clock()

    # Test one more than limit (could extract this limit to be a global var)
    try:
        m = isSecretAdditive(secret, 1000000001)
        if m is not largePrimeMessage:
            failed = True
            message = 'Failed to break when given a barely overlarge number for primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)
    

    ### ------------------------ ###
    ### Way Large Prime Test     ###
    ### ------------------------ ###
    reportTestStart('Way Large Prime')
    failed = False
    message = ''
    start = time.clock()

    # Test random lots more than limit number
    try:
        m = isSecretAdditive(secret, 35206089431)
        if m is not largePrimeMessage:
            failed = True
            message = 'Failed to break when given a very overlarge number for primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Prime Generation Test    ###
    ### ------------------------ ###
    reportTestStart('Prime Generation')
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
    start = time.clock()

    try:
        myPrimes = subPrimes(1000)

        if len(primesGold) != len(myPrimes):
            failed = True
            message = 'Length of prime arrays are different'
        else:
            for i in range(len(primesGold)):
                if primesGold[i] != myPrimes[i]:
                    failed = True
                    message = 'primesGold[{id}] ({pg}) did not match myPrimes[{id}] ({mp})'\
                        .format(id=i, pg=str(primesGold[i]), mp=str(myPrimes[i]))
                    break;
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Simple Additive 1 Test   ###
    ### ------------------------ ###
    reportTestStart('Simple Additive 1')
    failed = False
    message = ''
    start = time.clock()

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

    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Simple Additive 2 Test   ###
    ### ------------------------ ###
    reportTestStart('Simple Additive 2')
    failed = False
    message = ''
    start = time.clock()

    # Test with a super simple secret that is definitely additive
    # (Just returns the input)
    try:
        secret.changeFunction('superSimpleSecret')
        m = isSecretAdditive(secret, 1000)
        if m is not successMessage:
            failed = True
            message = 'Failed to identify super simple secret as additive for larger set of primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Non Additive 1 Test      ###
    ### ------------------------ ###
    reportTestStart('Non Additive 1')
    failed = False
    message = ''
    start = time.clock()

    # Test with a simple secret that is definitely non-additive
    # (Just squares input)
    try:
        secret.changeFunction('nonAdditiveSecret')
        m = isSecretAdditive(secret, 20)
        if m is not failedMessage:
            failed = True
            message = 'Failed to identify secret as non additive'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)


    ### ------------------------ ###
    ### Non Additive 2 Test      ###
    ### ------------------------ ###
    reportTestStart('Non Additive 2')
    failed = False
    message = ''
    start = time.clock()

    # Test with a simple secret that is definitely non-additive
    # (Just squares input)
    try:
        secret.changeFunction('nonAdditiveSecret')
        m = isSecretAdditive(secret, 1000)
        if m is not failedMessage:
            failed = True
            message = 'Failed to identify secret as non additive for larger set of primes'
    except:
        failed = True
        message = 'Test threw an exception\n\t' + str(sys.exc_info()[0])

    reportTestResults(failed, start, message)


### Have a common format for test names
def reportTestStart(testName):
    print testName + ' Test\n------------------------'

### Have a common format for test results
def reportTestResults(failed, start, message=''):
    p = '\t{pf} - Time Elapsed : {te:,.3f} s'\
        .format(pf=('Failed' if failed else 'Passed'), te=(time.clock() - start))

    # If it failed and had a message, go ahead and print that too
    if failed and message:
        p = p + '\n\t' + message
    print p + '\n'


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

    if not args.test:
        m = isSecretAdditive(s, args.number)
        print str(m)
