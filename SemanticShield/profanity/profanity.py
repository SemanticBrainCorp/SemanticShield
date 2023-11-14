from profanity_check import predict, predict_prob
from better_profanity import profanity
import timeit

profanity.load_censor_words()

# two methods
#   'imprecise' = quick, very broad but lacking good support for leetspeak (alt-profanity-check)
#   'precise' = slower, less broad but good support for leetspeak (better_profanity)
# setting 'precise' mode triggers both checks

def quick_test(text):
    # 2 sec/1000 text
    result = predict([text])
    return result[0] == 1

def slow_test(text):
    # 18 sec/1000 text
    result = profanity.contains_profanity(text)
    return result

def check_profanity(text: str, precise:str = 'precise'):
    quick_result = quick_test(text)
    if precise=='precise' and not quick_result:
        slow_result = slow_test(text)
        return slow_result
    return quick_result

if __name__=='__main__':
    print(quick_test('You p1ec3 of sHit.'))
    print(quick_test('have a nice day'))
    print(slow_test('You p1ec3 of sHit.'))
    print(slow_test('have a nice day'))

    print(quick_test('are you an idiot'))
    print(slow_test('are you an idiot.'))

    print(predict_prob(['are you an idiot']))
    
