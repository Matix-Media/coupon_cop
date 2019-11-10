# coupon_cop
Manage your coupons and discounts simple with this little program on your local machine. (Server support comming soon)

## Commands

**Help**  
```> coupon_cop help```  
for help.

**Create new coupon**  
```> coupon_cop new_coupon <discount>```  
Creates a new coupon. Write your discout in the filed `<discount>`.

**Check for a coupon**  
```> coupon_cop check_coupon <data type (id/code)> <id/code>```  
Checks the state and info of a coupon. Write `code` in the field `<data type>` to search with the code or `id` if you want to search after id.

**Use a coupon**  
```> coupon_cop <data type (id/code)> <id/code>```  
to mark a coupon as used.

**Reset a coupon**  
```> coupon_cop reset_coupon <data type (id/code)> <id/code>```  
to unmark a coupon.
