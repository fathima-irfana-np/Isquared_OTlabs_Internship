# AI Exploratory Tests

## VT-01: Break email input with long string
* Navigate to '/'
* Enter '999999999999999999999999999999999999999999999999999999999999999' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-02: Poison email input with special characters
* Navigate to '/login'
* Enter '!@#$%^&*()' into 'Your email'
* Click 'Sign In'
* Verify: Error message or login failure

## VT-03: Exceed max limit of email input
* Navigate to '/register'
* Enter 'a' 256 times into 'Your email'
* Click 'Create Account'
* Verify: Error message or input field rejection

## VT-04: Cross-field contamination with extra characters
* Navigate to '/about'
* Enter 'test@example.com' into 'Your email'
* Copy and paste 'test@example.com ' with extra space into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-05: Empty required email field
* Navigate to '/services'
* Leave 'Your email' empty
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-06: Whitespaces-only in email input
* Navigate to '/services/weddings'
* Enter '   ' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-07: Min limit of email input
* Navigate to '/login'
* Enter 'a' into 'Your email'
* Click 'Sign In'
* Verify: Error message or login failure

## VT-08: Input with leading and trailing spaces
* Navigate to '/register'
* Enter ' test@example.com ' into 'Your email'
* Click 'Create Account'
* Verify: Error message or input field rejection

## VT-09: Test form abandonment on login page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Navigate to '/register'
* Verify: Form fields are cleared

## VT-10: Verify state persistence on register page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Navigate to '/about'
* Navigate back to '/register'
* Verify: Form fields retain values

## VT-11: Check form reset on services page
* Navigate to '/services'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/services/weddings'
* Navigate back to '/services'
* Verify: Form field is cleared

## VT-12: Test mid-form navigation on root page
* Navigate to '/'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/login'
* Navigate back to '/'
* Verify: Form field is cleared

## VT-13: Verify form abandonment on about page
* Navigate to '/about'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/services'
* Verify: Form field is cleared

## VT-14: Check state transition on services weddings page
* Navigate to '/services/weddings'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/about'
* Navigate back to '/services/weddings'
* Verify: Form field retains value

## VT-15: Test form modification on login page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Click 'Dismiss'
* Enter 'new@example.com' into 'Your email'
* Verify: Form field is updated

## VT-16: Verify form reset on root page
* Navigate to '/'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/register'
* Navigate back to '/'
* Verify: Form field is cleared

## VT-17: Check form abandonment on register page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Enter 'on' into 'on'
* Navigate to '/about'
* Verify: Form fields are cleared

## VT-18: Break the email input with a very large number
* Navigate to '/'
* Enter '9999999999' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-19: Test the email input with a very small decimal
* Navigate to '/about'
* Enter '0.0001' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-20: Probe the email input with zero
* Navigate to '/services'
* Enter '0' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-21: Break the email input with one below minimum
* Navigate to '/services/weddings'
* Enter '-1' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-22: Test the email input with one above maximum
* Navigate to '/'
* Enter '2147483648' into 'Your email'
* Click 'Dismiss'
* Verify: Error message or input field rejection

## VT-23: Probe the email input with exact minimum allowed value
* Navigate to '/about'
* Enter '1' into 'Your email'
* Click 'Dismiss'
* Verify: Input field acceptance

## VT-24: Break the email input with exact maximum allowed value
* Navigate to '/services'
* Enter '2147483647' into 'Your email'
* Click 'Dismiss'
* Verify: Input field acceptance

## VT-25: Test the on input with a very large number on the login page
* Navigate to '/login'
* Enter '9999999999' into 'on'
* Click 'Sign In'
* Verify: Error message or input field rejection

## VT-26: Probe the on input with zero on the register page
* Navigate to '/register'
* Enter '0' into 'on'
* Click 'Create Account'
* Verify: Error message or input field rejection

## VT-27: Break navigation between login and register pages
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Click 'Dismiss'
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Verify: Registration form is populated with previously entered email

## VT-28: Disrupt about page with dismiss button
* Navigate to '/about'
* Enter 'test@example.com' into 'Your email'
* Click 'Dismiss'
* Navigate to '/services'
* Verify: Services page is displayed without errors

## VT-29: Test independent operation of services and weddings pages
* Navigate to '/services'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/services/weddings'
* Enter 'test2@example.com' into 'Your email'
* Verify: Weddings page has independent email input

## VT-30: Interrupt login flow with navigation to about page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/about'
* Click 'Dismiss'
* Verify: Login page is re-displayed with previously entered email

## VT-31: Verify retention of email input across page navigation
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/register'
* Navigate back to '/login'
* Verify: Login page is displayed with previously entered email

## VT-32: Test navigation between services and weddings pages with email input
* Navigate to '/services'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/services/weddings'
* Enter 'test2@example.com' into 'Your email'
* Navigate back to '/services'
* Verify: Services page is displayed with original email input

## VT-33: Break register page with dismiss button and navigation
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Click 'Dismiss'
* Navigate to '/login'
* Verify: Login page is displayed without errors

## VT-34: Test independent operation of about and services pages
* Navigate to '/about'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/services'
* Enter 'test2@example.com' into 'Your email'
* Verify: Services page has independent email input

## VT-35: Interrupt register flow with navigation to login page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Navigate to '/login'
* Click 'Dismiss'
* Verify: Register page is re-displayed with previously entered email

## VT-36: Break mode switching on login page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Click 'Sign In'
* Click 'Dismiss'
* Verify: Login form resets

## VT-37: Test rapid mode switching on register page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Click 'Create Account'
* Click 'Dismiss'
* Click 'Create Account'
* Verify: No UI flicker or errors

## VT-38: Verify mode switch retains values on login page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Click 'Dismiss'
* Click 'Sign In'
* Verify: Email value retained

## VT-39: Break mode switching with incomplete form on register page
* Navigate to '/register'
* Click 'Create Account'
* Enter 'test@example.com' into 'Your email'
* Click 'Create Account'
* Verify: Form submission fails

## VT-40: Test mode switch before filling form on login page
* Navigate to '/login'
* Click 'Sign In'
* Enter 'test@example.com' into 'Your email'
* Click 'Sign In'
* Verify: Login fails

## VT-41: Verify mode switch changes labels correctly on register page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Click 'Create Account'
* Click 'Dismiss'
* Verify: Labels change correctly

## VT-42: Break rapid mode switching on login page
* Navigate to '/login'
* Click 'Sign In'
* Click 'Dismiss'
* Click 'Sign In'
* Click 'Dismiss'
* Verify: No UI errors or crashes

## VT-43: Test mode switch with multiple form submissions on register page
* Navigate to '/register'
* Enter 'test@example.com' into 'Your email'
* Click 'Create Account'
* Click 'Create Account'
* Verify: No duplicate submissions

## VT-44: Verify mode switch retains state on login page
* Navigate to '/login'
* Enter 'test@example.com' into 'Your email'
* Click 'Sign In'
* Click 'Dismiss'
* Click 'Sign In'
* Verify: State retained correctly
