# AI Exploratory Tests

## VT-01: Break loan calculator with extreme loan amount
* Navigate to '/loan-calculator.html'
* Enter '999999999' into 'cloanamount'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-02: Poison mortgage calculator with special characters
* Navigate to '/mortgage-calculator.html'
* Enter '!@#$%' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or calculator crash

## VT-03: Torture interest calculator with negative interest rate
* Navigate to '/interest-calculator.html'
* Enter '-0.01' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or incorrect calculation

## VT-04: Contaminate auto loan calculator with cross-field input
* Navigate to '/auto-loan-calculator.html'
* Enter '12345' into 'csaleprice'
* Copy '12345' and paste into 'cdownpayment' with extra characters 'abc'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-05: Break payment calculator with empty loan amount
* Navigate to '/payment-calculator.html'
* Leave 'cloanamount' empty
* Click 'Search'
* Verify: Error message or calculator crash

## VT-06: Poison retirement calculator with whitespace-only input
* Navigate to '/retirement-calculator.html'
* Enter '   ' into 'cagenow'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-07: Torture amortization calculator with maximum loan term exceeded
* Navigate to '/amortization-calculator.html'
* Enter '1000' into 'cloantermmonth'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-08: Contaminate financial calculator with long string input
* Navigate to '/financial-calculator.html'
* Enter '999999999999999999999' into 'calcSearchTerm'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-09: Break calculator with special characters in search term
* Navigate to '/'
* Enter '!@#$%' into 'calcSearchTerm'
* Click 'Search'
* Verify: Error message or calculator crash

## VT-10: Poison mortgage calculator with extreme interest rate
* Navigate to '/mortgage-calculator.html'
* Enter '1000' into 'cinterestrate'
* Click 'Get pre-approval'
* Verify: Error message or calculator crash

## VT-11: Break form persistence on loan calculator
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Verify: Form fields are cleared

## VT-12: Test state transition on mortgage calculator
* Navigate to '/mortgage-calculator.html'
* Enter '200000' into 'chouseprice'
* Enter '20' into 'cdownpayment'
* Click 'Get pre-approval'
* Navigate back to '/mortgage-calculator.html'
* Verify: Form fields retain previous values

## VT-13: Explore interest calculator state persistence
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Enter '5' into 'cyears'
* Click 'Search'
* Navigate to '/'
* Navigate back to '/interest-calculator.html'
* Verify: Form fields are reset

## VT-14: Investigate auto loan calculator form abandonment
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Enter '10' into 'cloanterm'
* Navigate to '/loan-calculator.html'
* Navigate back to '/auto-loan-calculator.html'
* Verify: Form fields are reset

## VT-15: Test payment calculator result update
* Navigate to '/payment-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Enter '6' into 'cloanterm'
* Click 'Search'
* Verify: Result is updated with new loan term

## VT-16: Examine retirement calculator input modification
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Enter '65' into 'cretireage'
* Click 'Search'
* Enter '35' into 'cagenow'
* Click 'Search'
* Verify: Result is updated with new age

## VT-17: Break amortization calculator form submission
* Navigate to '/amortization-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Enter '6' into 'cloanterm'
* Click 'Search'
* Verify: Result is updated with new loan term

## VT-18: Investigate financial calculator search functionality
* Navigate to '/financial-calculator.html'
* Enter 'loan' into 'calcSearchTerm'
* Click 'Search'
* Navigate back to '/financial-calculator.html'
* Verify: Search results are retained

## VT-19: Test calculator.net homepage search
* Navigate to '/'
* Enter 'sin' into 'calcSearchTerm'
* Click 'Search'
* Navigate back to '/'
* Verify: Search results are reset

## VT-20: Break the loan calculator with minimum loan amount
* Navigate to '/loan-calculator.html'
* Enter '0' into 'cloanamount'
* Click 'Search'
* Verify: Error message or invalid result

## VT-21: Break the loan calculator with maximum loan amount
* Navigate to '/loan-calculator.html'
* Enter '9999999999' into 'cloanamount'
* Click 'Search'
* Verify: Error message or invalid result

## VT-22: Break the loan calculator with minimum interest rate
* Navigate to '/loan-calculator.html'
* Enter '0' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or invalid result

## VT-23: Break the loan calculator with maximum interest rate
* Navigate to '/loan-calculator.html'
* Enter '100' into 'cinterestrate'
* Click 'Search'
* Verify: Error message or invalid result

## VT-24: Break the mortgage calculator with minimum house price
* Navigate to '/mortgage-calculator.html'
* Enter '0' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or invalid result

## VT-25: Break the mortgage calculator with maximum house price
* Navigate to '/mortgage-calculator.html'
* Enter '9999999999' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Error message or invalid result

## VT-26: Break the auto loan calculator with minimum sale price
* Navigate to '/auto-loan-calculator.html'
* Enter '0' into 'csaleprice'
* Click 'Search'
* Verify: Error message or invalid result

## VT-27: Break the interest calculator with minimum starting principle
* Navigate to '/interest-calculator.html'
* Enter '0' into 'cstartingprinciple'
* Click 'Search'
* Verify: Error message or invalid result

## VT-28: Break the payment calculator with minimum loan amount
* Navigate to '/payment-calculator.html'
* Enter '0' into 'cloanamount'
* Click 'Search'
* Verify: Error message or invalid result

## VT-29: Break the retirement calculator with minimum age
* Navigate to '/retirement-calculator.html'
* Enter '0' into 'cagenow'
* Click 'Search'
* Verify: Error message or invalid result

## VT-30: Break loan calculator by navigating away and back
* Navigate to '/loan-calculator.html'
* Enter '1000' into 'cloanamount'
* Navigate to '/mortgage-calculator.html'
* Navigate to '/loan-calculator.html'
* Verify: Loan amount is retained as '1000'

## VT-31: Disrupt interest calculator with unexpected navigation
* Navigate to '/interest-calculator.html'
* Enter '100' into 'cstartingprinciple'
* Click 'Search'
* Navigate to '/payment-calculator.html'
* Navigate to '/interest-calculator.html'
* Verify: Interest calculator results are reset

## VT-32: Test retirement calculator's resilience to mid-flow navigation
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Navigate to '/loan-calculator.html'
* Navigate to '/retirement-calculator.html'
* Verify: Retirement calculator inputs are cleared

## VT-33: Investigate amortization calculator's behavior after navigating away
* Navigate to '/amortization-calculator.html'
* Enter '50000' into 'cloanamount'
* Navigate to '/auto-loan-calculator.html'
* Navigate to '/amortization-calculator.html'
* Verify: Amortization calculator inputs are retained

## VT-34: Evaluate financial calculator's response to interrupted search
* Navigate to '/financial-calculator.html'
* Enter 'mortgage' into 'calcSearchTerm'
* Navigate to '/mortgage-calculator.html'
* Click 'Back'
* Verify: Financial calculator search results are displayed

## VT-35: Assess loan calculator's ability to recover from navigation chaos
* Navigate to '/loan-calculator.html'
* Enter '2000' into 'cloanamount'
* Navigate to '/interest-calculator.html'
* Navigate to '/loan-calculator.html'
* Click 'Clear'
* Verify: Loan calculator inputs are cleared

## VT-36: Examine payment calculator's reaction to unexpected navigation
* Navigate to '/payment-calculator.html'
* Enter '1000' into 'cloanamount'
* Navigate to '/retirement-calculator.html'
* Navigate to '/payment-calculator.html'
* Verify: Payment calculator inputs are retained

## VT-37: Probe auto loan calculator's defenses against navigation attacks
* Navigate to '/auto-loan-calculator.html'
* Enter '15000' into 'csaleprice'
* Navigate to '/loan-calculator.html'
* Navigate to '/auto-loan-calculator.html'
* Click 'Search'
* Verify: Auto loan calculator results are displayed

## VT-38: Investigate mortgage calculator's vulnerability to navigation exploits
* Navigate to '/mortgage-calculator.html'
* Enter '200000' into 'chouseprice'
* Navigate to '/financial-calculator.html'
* Navigate to '/mortgage-calculator.html'
* Verify: Mortgage calculator inputs are retained

## VT-39: Break loan calculator by switching between two calculation modes
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'c2loanamount'
* Enter '5' into 'c2loanterm'
* Click 'Clear'
* Enter '10000' into 'c3loanamount'
* Enter '5' into 'c3loanterm'
* Verify: Calculator retains values after switching between modes

## VT-40: Stress-test toggle buttons on interest calculator
* Navigate to '/interest-calculator.html'
* Click 'x'
* Click 'Clear'
* Click 'x'
* Enter '1000' into 'cstartingprinciple'
* Click 'Search'
* Verify: No UI flicker or errors after rapid toggle button clicks

## VT-41: Test mode switching on auto loan calculator
* Navigate to '/auto-loan-calculator.html'
* Enter '20000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Click 'x'
* Enter '20000' into 'csaleprice'
* Enter '5' into 'cloanterm'
* Verify: Calculator retains values after mode switching

## VT-42: Rapidly apply and unapply modes on payment calculator
* Navigate to '/payment-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'x'
* Click 'Clear'
* Click 'x'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Verify: No UI errors or flicker after rapid mode switching

## VT-43: Test label changes on retirement calculator
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Enter '60' into 'cretireage'
* Click 'x'
* Enter '30' into 'cagenow'
* Enter '60' into 'cretireage'
* Verify: Old values still map to new labels after mode switching

## VT-44: Break amortization calculator by switching between modes
* Navigate to '/amortization-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Clear'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Verify: Calculator retains values after switching between modes

## VT-45: Stress-test mode switching on loan calculator
* Navigate to '/loan-calculator.html'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'x'
* Click 'Clear'
* Click 'x'
* Enter '10000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Verify: No UI errors or flicker after rapid mode switching

## VT-46: Test UI state changes on interest calculator
* Navigate to '/interest-calculator.html'
* Enter '1000' into 'cstartingprinciple'
* Click 'x'
* Enter '1000' into 'cstartingprinciple'
* Click 'Clear'
* Verify: UI state changes correctly after mode switching

## VT-47: Test mode switching on financial calculator
* Navigate to '/financial-calculator.html'
* Enter '1000' into 'calcSearchTerm'
* Click 'Search'
* Enter '1000' into 'calcSearchTerm'
* Click 'Search'
* Verify: Calculator retains values after mode switching

## VT-48: Trigger calculation error and verify recovery
* Navigate to '/loan-calculator.html'
* Enter '0' into 'c2loanamount'
* Click 'Search'
* Enter '100' into 'c2loanamount'
* Click 'Search'
* Verify: Successful calculation result

## VT-49: Submit empty form and verify error handling
* Navigate to '/mortgage-calculator.html'
* Click 'Get pre-approval'
* Verify error message
* Enter '100000' into 'chouseprice'
* Click 'Get pre-approval'
* Verify: Successful pre-approval result

## VT-50: Submit with invalid value and verify error clearance
* Navigate to '/interest-calculator.html'
* Enter 'abc' into 'cstartingprinciple'
* Click 'Search'
* Verify error message
* Enter '1000' into 'cstartingprinciple'
* Click 'Search'
* Verify: Successful calculation result

## VT-51: Clear all fields after successful calculation and verify reset
* Navigate to '/payment-calculator.html'
* Enter '1000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Click 'Clear'
* Verify all fields are cleared
* Verify: All fields are empty

## VT-52: Enter valid data, click Clear/Reset, and verify all fields are cleared
* Navigate to '/retirement-calculator.html'
* Enter '30' into 'cagenow'
* Enter '60' into 'cretireage'
* Click 'Clear'
* Verify all fields are cleared
* Verify: All fields are empty

## VT-53: Trigger division by zero error and verify recovery
* Navigate to '/loan-calculator.html'
* Enter '0' into 'c2loanterm'
* Click 'Search'
* Verify error message
* Enter '5' into 'c2loanterm'
* Click 'Search'
* Verify: Successful calculation result

## VT-54: Submit empty form and verify error handling
* Navigate to '/amortization-calculator.html'
* Click 'Search'
* Verify error message
* Enter '1000' into 'cloanamount'
* Enter '5' into 'cloanterm'
* Click 'Search'
* Verify: Successful calculation result

## VT-55: Enter invalid value, correct it, and verify successful calculation
* Navigate to '/auto-loan-calculator.html'
* Enter 'abc' into 'csaleprice'
* Click 'Search'
* Verify error message
* Enter '20000' into 'csaleprice'
* Click 'Search'
* Verify: Successful calculation result

## VT-56: Clear all fields after successful calculation and verify reset
* Navigate to '/financial-calculator.html'
* Enter '100' into 'calcSearchTerm'
* Click 'Search'
* Click 'Clear'
* Verify all fields are cleared
* Verify: All fields are empty

## VT-57: Trigger calculation error and verify recovery
* Navigate to '/mortgage-calculator.html'
* Enter '0' into 'cdownpayment'
* Click 'Get pre-approval'
* Verify error message
* Enter '10000' into 'cdownpayment'
* Click 'Get pre-approval'
* Verify: Successful pre-approval result
