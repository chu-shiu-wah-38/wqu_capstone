import pandas as pd
import ValueAtRisk as Risk

PASSED = ' - success'
FAILED = ' - failed, actual is '


# Set DataFrame data
data = {'Close':range(1,251)}
df = pd.DataFrame(data)


'''
TestVaR990
Result should: 4
Explanation:  0.01 x 250 returns is 2.5, which is 3 (next whole number).  
            The next return's value is 4.
'''
var_990 = Risk.value_at_risk(df, 0.01)
if var_990['Close'] == 4:
    print('TestVaR990' + PASSED)
else:
    print('TestVaR990' + FAILED + str(var_990['Close']))


'''
TestVaR975
Result should: 8
Explanation:  0.025 x 250 returns is 6.25, which is 7 (next whole number).  
            The next return's value is 8.
'''
var_975 = Risk.value_at_risk(df, 0.025)
if var_975['Close'] == 8:
    print('TestVaR975' + PASSED)
else:
    print('TestVaR975' + FAILED + str(var_975['Close']))


'''
TestES990
Result should: 2
Explanation:  VaR is 4.  ES is average(range(1 to 3)) 
                                => 6 / 3  
                                => 2 
'''
es990 = Risk.expected_shortfall(df, 0.01)
if es990['Close'] == 2:
    print('TestES990' + PASSED)
else:
    print('TestES990' + FAILED + str(es990['Close']))


'''
TestES975
Result should: 4
Explanation:  VaR is 8.  ES is average(range(1 to 7)) 
                                => 28 / 7  
                                => 4 
'''
es = Risk.expected_shortfall(df, 0.025)
if es['Close'] == 4:
    print('TestES975' + PASSED)
else:
    print('TestES975' + FAILED + str(es['Close']))
