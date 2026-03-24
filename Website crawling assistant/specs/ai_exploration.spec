# AI Exploratory Tests

## VT-01: Break form submission by rapid input filling
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Sign In'
* Enter 'test2@example.com' into 'Your email'
* Enter 'off' into 'on'
* Click 'Sign In'
* Verify: Validation failure for duplicate submission

## VT-02: Test form submission with empty optional fields
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Click 'Create Account'
* Verify: No UI errors or crashes

## VT-03: Break form submission by multiple rapid clicks
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Sign In'
* Click 'Sign In'
* Click 'Sign In'
* Verify: Error message for multiple submissions

## VT-04: Test form submission with required fields only
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Click 'Sign In'
* Verify: Validation failure for missing 'on' field

## VT-05: Break form submission by clearing and refilling
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Dismiss'
* Enter 'test2@example.com' into 'Your email'
* Enter 'off' into 'on'
* Click 'Create Account'
* Verify: No UI errors or crashes

## VT-06: Test form submission with rapid input changes
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Enter 'test2@example.com' into 'Your email'
* Enter 'off' into 'on'
* Click 'Sign In'
* Verify: Validation failure for rapid input changes

## VT-07: Break form submission by multiple submissions with same values
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Sign In'
* Click 'Sign In'
* Verify: Error message for duplicate submission

## VT-08: Test form submission with different input values
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Create Account'
* Enter 'test2@example.com' into 'Your email'
* Enter 'off' into 'on'
* Click 'Create Account'
* Verify: No UI errors or crashes

## VT-09: Break form submission by rapid form clearing and refilling
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Dismiss'
* Enter 'test2@example.com' into 'Your email'
* Enter 'off' into 'on'
* Click 'Dismiss'
* Enter 'test3@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Sign In'
* Verify: Validation failure for rapid form clearing and refilling
