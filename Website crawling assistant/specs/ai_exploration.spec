# AI Exploratory Tests

## VT-01: Break the loan calculator with a very large loan amount
* Navigate to '/loan-calculator.html'
* Enter '999999999' into 'cloanamount'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-02: Poison the interest calculator with a negative interest rate
* Navigate to '/interest-calculator.html'
* Enter '-0.01' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or incorrect calculation

## VT-03: Overflow the payment calculator with a very large loan term
* Navigate to '/payment-calculator.html'
* Enter '100000' into 'cloanterm'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-04: Contaminate the auto loan calculator with a non-numeric trade-in value
* Navigate to '/auto-loan-calculator.html'
* Enter 'abc' into 'ctradeinvalue'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-05: Break the retirement calculator with a very large annual savings amount
* Navigate to '/retirement-calculator.html'
* Enter '999999999' into 'cannualsave'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-06: Poison the amortization calculator with a negative loan amount
* Navigate to '/amortization-calculator.html'
* Enter '-1000' into 'cloanamount'
* Click 'Search'
* Verify: Error message or incorrect calculation

## VT-07: Overflow the mortgage calculator with a very large home price
* Navigate to '/mortgage-calculator.html'
* Enter '1000000000' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or calculator crash

## VT-08: Contaminate the financial calculator with a non-numeric search term
* Navigate to '/financial-calculator.html'
* Enter 'abc' into 'calcSearchTerm'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-09: Break the calculator on the main page with a very large search term
* Navigate to '/'
* Enter '999999999999999999' into 'calcSearchTerm'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-10: Poison the sign-in page with a very large email address
* Navigate to '/my-account/sign-in.php'
* Enter 'a' * 1000 into 'email'
* Click 'submit'
* Verify: Error message or calculator crash

## VT-11: Test state transition on loan calculator
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Verify: Form fields are cleared

## VT-12: Test form abandonment on mortgage calculator
* Navigate to '/mortgage-calculator.html'
* Enter '200000' into 'chouseprice'
* Enter '20' into 'cdownpayment'
* Navigate to '/loan-calculator.html'
* Verify: Mortgage calculator form is reset

## VT-13: Test state persistence on interest calculator
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Enter '5' into 'cinterestrate'
* Navigate to '/payment-calculator.html'
* Navigate back to '/interest-calculator.html'
* Verify: Interest calculator form fields retain values

## VT-14: Test calculate and modify on auto loan calculator
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Enter '6' into 'cloanterm'
* Click 'Search'
* Verify: Calculator output updates with new loan term

## VT-15: Test browser back button on retirement calculator
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Enter '60' into 'cretireage'
* Click 'Search'
* Navigate back to '/retirement-calculator.html'
* Verify: Retirement calculator form fields are reset

## VT-16: Test submit and change inputs on amortization calculator
* Navigate to '/amortization-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Enter '6' into 'cloanterm'
* Click 'Search'
* Verify: Calculator output updates with new loan term

## VT-17: Test partial form fill on payment calculator
* Navigate to '/payment-calculator.html'
* Enter '10000' into 'cloanamount'
* Navigate to '/loan-calculator.html'
* Navigate back to '/payment-calculator.html'
* Verify: Payment calculator form fields retain values

## VT-18: Test change value mid-form on financial calculator
* Navigate to '/financial-calculator.html'
* Enter 'finance' into 'calcSearchTerm'
* Navigate to '/loan-calculator.html'
* Navigate back to '/financial-calculator.html'
* Verify: Financial calculator form field is reset

## VT-19: Test state transition on mortgage calculator
* Navigate to '/mortgage-calculator.html'
* Enter '200000' into 'chouseprice'
* Enter '20' into 'cdownpayment'
* Click 'Get pre-approval'
* Navigate to '/loan-calculator.html'
* Verify: Mortgage calculator form is reset

## VT-20: Test form abandonment on interest calculator
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Enter '5' into 'cinterestrate'
* Navigate to '/payment-calculator.html'
* Verify: Interest calculator form is reset

## VT-21: Break the loan calculator with minimum loan amount
* Navigate to '/loan-calculator.html'
* Enter '0' into 'cloanamount'
* Click 'Search'
* Verify: Error message or invalid result

## VT-22: Break the loan calculator with maximum loan amount
* Navigate to '/loan-calculator.html'
* Enter '9999999999' into 'cloanamount'
* Click 'Search'
* Verify: Error message or invalid result

## VT-23: Break the loan calculator with minimum loan term
* Navigate to '/loan-calculator.html'
* Enter '0' into 'cloanterm'
* Click 'Search'
* Verify: Error message or invalid result

## VT-24: Break the loan calculator with maximum loan term
* Navigate to '/loan-calculator.html'
* Enter '999' into 'cloanterm'
* Click 'Search'
* Verify: Error message or invalid result

## VT-25: Break the loan calculator with very small interest rate
* Navigate to '/loan-calculator.html'
* Enter '0.0001' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or invalid result

## VT-26: Break the loan calculator with very large interest rate
* Navigate to '/loan-calculator.html'
* Enter '999' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or invalid result

## VT-27: Break the mortgage calculator with minimum house price
* Navigate to '/mortgage-calculator.html'
* Enter '0' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or invalid result

## VT-28: Break the mortgage calculator with maximum house price
* Navigate to '/mortgage-calculator.html'
* Enter '9999999999' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or invalid result

## VT-29: Break the auto loan calculator with minimum sale price
* Navigate to '/auto-loan-calculator.html'
* Enter '0' into 'csaleprice'
* Click 'Search'
* Verify: Error message or invalid result

## VT-30: Break the interest calculator with minimum starting principle
* Navigate to '/interest-calculator.html'
* Enter '0' into 'cstartingprinciple'
* Click 'Search'
* Verify: Error message or invalid result

## VT-31: Break loan calculator by navigating away and back
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Navigate to '/mortgage-calculator.html'
* Navigate to '/loan-calculator.html'
* Verify: Loan amount field is empty

## VT-32: Test navigation between calculators
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Navigate to '/interest-calculator.html'
* Enter '5000' into 'cstartingprinciple'
* Navigate to '/auto-loan-calculator.html'
* Verify: Sale price field is empty

## VT-33: Verify independent operation of multiple calculators
* Navigate to '/payment-calculator.html'
* Enter '10000' into 'cloanamount'
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Navigate to '/payment-calculator.html'
* Verify: Loan amount field is empty

## VT-34: Test calculation interruption by navigation
* Navigate to '/amortization-calculator.html'
* Enter '20000' into 'cloanamount'
* Navigate to '/financial-calculator.html'
* Navigate to '/amortization-calculator.html'
* Verify: Loan amount field is empty

## VT-35: Break calculator by changing mode and navigating back
* Navigate to '/mortgage-calculator.html'
* Enter '300000' into 'chouseprice'
* Click 'Get pre-approval'
* Navigate to '/loan-calculator.html'
* Navigate to '/mortgage-calculator.html'
* Verify: House price field is empty

## VT-36: Test navigation between related pages
* Navigate to '/loan-calculator.html'
* Enter '5000' into 'cloanamount'
* Click 'Search'
* Navigate to '/financial-calculator.html'
* Navigate to '/loan-calculator.html'
* Verify: Loan amount field is empty

## VT-37: Verify calculation retention after navigation
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Navigate to '/payment-calculator.html'
* Navigate to '/interest-calculator.html'
* Verify: Starting principle field is empty

## VT-38: Break calculator by opening multiple instances
* Navigate to '/auto-loan-calculator.html'
* Enter '15000' into 'csaleprice'
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Navigate to '/auto-loan-calculator.html'
* Verify: Sale price field is empty

## VT-39: Test navigation between calculators with search
* Navigate to '/financial-calculator.html'
* Enter 'mortgage' into 'calcSearchTerm'
* Click 'Search'
* Navigate to '/mortgage-calculator.html'
* Navigate to '/financial-calculator.html'
* Verify: Search term field is empty

## VT-40: Verify calculation interruption by header link
* Navigate to '/loan-calculator.html'
* Enter '8000' into 'cloanamount'
* Navigate to '/'
* Navigate to '/loan-calculator.html'
* Verify: Loan amount field is empty

## VT-41: Break loan calculator by switching between two calculation modes
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'c2loanamount'
* Enter '5' into 'c2loanterm'
* Click 'Search'
* Verify: Calculator displays correct results for both loan amounts

## VT-42: Test mode switching in interest calculator
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Enter '5' into 'cyears'
* Click 'Clear'
* Enter '1000' into 'cstartingprinciple'
* Enter '5' into 'cyears'
* Click 'Search'
* Verify: Calculator displays correct interest results

## VT-43: Rapidly apply and unapply a mode in payment calculator
* Navigate to '/payment-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'x'
* Click 'Clear'
* Click 'Search'
* Verify: Calculator does not display any errors

## VT-44: Test UI state changes in retirement calculator
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Enter '65' into 'cretireage'
* Click 'Clear'
* Enter '30' into 'cagenow'
* Enter '65' into 'cretireage'
* Click 'Search'
* Verify: Calculator displays correct retirement results

## VT-45: Switch between two calculation modes in amortization calculator
* Navigate to '/amortization-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Verify: Calculator displays correct amortization results

## VT-46: Test mode switching in auto loan calculator
* Navigate to '/auto-loan-calculator.html'
* Enter '10000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Verify: Calculator displays correct auto loan results

## VT-47: Rapidly apply and unapply a mode in mortgage calculator
* Navigate to '/mortgage-calculator.html'
* Enter '100000' into 'chouseprice'
* Enter '20' into 'cloanterm'
* Click 'Clear'
* Enter '100000' into 'chouseprice'
* Enter '20' into 'cloanterm'
* Click 'x'
* Click 'Clear'
* Click 'Get pre-approval'
* Verify: Calculator does not display any errors

## VT-48: Test UI state changes in financial calculator
* Navigate to '/financial-calculator.html'
* Click 'Search'
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Verify: Calculator displays correct financial results

## VT-49: Break calculator by switching between two calculation modes rapidly
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Click 'Clear'
* Click 'Search'
* Verify: Calculator does not crash or display any errors

## VT-50: Test mode switching in all calculators
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Navigate to '/mortgage-calculator.html'
* Enter '100000' into 'chouseprice'
* Enter '20' into 'cloanterm'
* Click 'Get pre-approval'
* Navigate to '/auto-loan-calculator.html'
* Enter '10000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Verify: All calculators display correct results

## VT-51: Trigger calculation error and verify recovery
* Navigate to '/loan-calculator.html'
* Enter '0' into 'c2loanamount'
* Click 'Search'
* Enter '100' into 'c2loanamount'
* Click 'Search'
* Verify: Calculation result is displayed without errors

## VT-52: Test error handling for empty form submission
* Navigate to '/mortgage-calculator.html'
* Click 'Get pre-approval'
* Note error message
* Enter '100000' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message is cleared and calculation result is displayed

## VT-53: Verify invalid input error recovery
* Navigate to '/interest-calculator.html'
* Enter '-1' into 'cstartingprinciple'
* Click 'Search'
* Note error message
* Enter '1000' into 'cstartingprinciple'
* Click 'Search'
* Verify: Error message is cleared and calculation result is displayed

## VT-54: Test divide by zero error handling
* Navigate to '/'
* Enter '0' into 'scirdsetting'
* Click '/'
* Note error message
* Enter '1' into 'scirdsetting'
* Click '/'
* Verify: Error message is cleared and calculation result is displayed

## VT-55: Verify clear all fields functionality
* Navigate to '/payment-calculator.html'
* Enter '1000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Enter '5' into 'cinterestrate'
* Click 'Search'
* Click 'Clear'
* Click 'Search'
* Verify: Error message is displayed for empty form submission

## VT-56: Test reset functionality after successful calculation
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Enter '5' into 'cinterestrate'
* Click 'Search'
* Click 'x'
* Click 'Search'
* Verify: Error message is displayed for empty form submission

## VT-57: Verify error handling for invalid input and subsequent valid input
* Navigate to '/retirement-calculator.html'
* Enter '-1' into 'cagenow'
* Click 'Search'
* Note error message
* Enter '30' into 'cagenow'
* Click 'Search'
* Verify: Error message is cleared and calculation result is displayed

## VT-58: Test calculation error recovery after invalid input
* Navigate to '/amortization-calculator.html'
* Enter '0' into 'cloanamount'
* Click 'Search'
* Note error message
* Enter '1000' into 'cloanamount'
* Click 'Search'
* Verify: Error message is cleared and calculation result is displayed

## VT-59: Verify error handling for empty form submission after successful calculation
* Navigate to '/financial-calculator.html'
* Enter '100' into 'calcSearchTerm'
* Click 'Search'
* Click 'Clear'
* Click 'Search'
* Verify: Error message is displayed for empty form submission

## VT-60: Test error recovery after division by zero error
* Navigate to '/'
* Enter '1' into 'scirdsetting'
* Click '1/x'
* Enter '0' into 'scirdsetting'
* Click '1/x'
* Note error message
* Enter '1' into 'scirdsetting'
* Click '1/x'
* Verify: Error message is cleared and calculation result is displayed
