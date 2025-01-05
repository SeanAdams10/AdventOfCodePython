# Register A: 32916674
# Register B: 0
# Register C: 0

# Program: 2,4
#         1,1,
#         7,5
#         0,3
#         1,4
#         4,0
#         5,5
#         3,0


# 3,0: JNZ 0
#     if A is not zero, jump to 0
#      This means that A is zero on the last attempt

# 5,5: OUT 5
#     output the value of register B mod 8
#     output is 0, meaning that B is a multiple of 8

# 4,0: BXC 0
#     the bitwise or of B and C is stored in B
#     which implies that B & C are multiples of 8 otherwise this would not work

# 1,4: BXL 4
#     B is XORed with 4
#     given that B above is a multiple of 8, then to get there, b has to be a multiple of 4
#     ??

# 0,3: ADV 3
#     A is divided by 2^3 and stored in A
#     is A a multiple of 8?

# 7,5: CDV 5
#     C is divided by 2^ B and stored in C
#     is C a multiple of 32?

# 1,1: BXL 1
#     B is XORed with 1
#     this makes B an even number

# 2,4: BST 4
#     B is set to the value of register B % 8

# Summary: The only operation impacting A's value is ADV 3, so we need to find values of A that generate remainders until the last bit



# Back prop:
# 16th iteration
# - Goal output is 0
# - A is 0 (since it doesn't loop)
          
# 3,0: JNZ 0
#     if A is not zero, jump to 0
#      This means that A is zero on the last attempt


# 5,5: OUT 5
#     output the value of register B mod 8
#     output is 0, meaning that B is a multiple of 8
# b1 is a multiple of 8 since output is zero
# b1 is multiple of 8

# 4,0: BXC 0
#     the bitwise or of B and C is stored in B

#     b2 = C XOR b1


# 1,4: BXL 4
#     B is XORed with 4
#     given that B above is a multiple of 8, then to get there, b has to be a multiple of 4
#     B3 xor 4 = B2
#     therefore B3 xor 4 = C xor b1
#     therefore B3 = C XOR b1 XOR 4

# 0,3: ADV 3
#     A is divided by 2^3 and stored in A
#     is A a multiple of 8?
#     A1 = int(A/8)

# 7,5: CDV 5
#     A is divided by 2^ B and stored in C
#     is C a multiple of 32?
#     C1 = int(A / 2^B3)
#     C1 = int(A / 2^(C xor b1 xor 4))
#     for this last iteration = C1 = 0 since A = 0


# 1,1: BXL 1
#     B is XORed with 1
#     this flips b to even or odd
#     B4 = B3 xor 1
#     B4 = C XOR b1 XOR 4 XOR 1
#     since C is zero - this is equivalent to 
#     B4 = B1 XOR 5





# 2,4: BST 4
#     B is set to the value of register B % 8




