word_size = 4
num_words = 2

def add_4bits(a,b, cin):
    a = a & 0x0f
    b = b & 0x0f

    result = (a + b + cin) & 0x1f
    print(f"Adding {a}, {b}, {cin} = {result}")

    return result



in1 = []
in2 = []
in3 = []
in4 = []
in5 = []
in6 = []
in7 = []
in8 = []
in9 = []

out1 = []
out2 = []
out3 = []
out4 = []
out5 = []


for a in range(2 ** word_size):
   for b in range(2 ** word_size):
       for c in range(2):
           sum_val = add_4bits(a, b, c)

           a0 = bool(a & 0x01)
           a1 = bool((a >> 1) & 0x01)
           a2 = bool((a >> 2) & 0x01)
           a3 = bool((a >> 3) & 0x01)

           b0 = bool(b & 0x01)
           b1 = bool((b >> 1) & 0x01)
           b2 = bool((b >> 2) & 0x01)
           b3 = bool((b >> 3) & 0x01)

           cin = bool(c & 0x01)


           s0 = bool(sum_val & 0x01)
           s1 = bool((sum_val >> 1) & 0x01)
           s2 = bool((sum_val >> 2) & 0x01)
           s3 = bool((sum_val >> 3) & 0x01)
           cout = bool((sum_val >> 4) & 0x01)

           in1.append(cin)
           in2.append(a0)
           in3.append(b0)
           in4.append(a1)
           in5.append(b1)
           in6.append(a2)
           in7.append(b2)
           in8.append(a3)
           in9.append(b3)

           out1.append(s0)
           out2.append(s1)
           out3.append(s2)
           out4.append(s3)
           out5.append(cout)


print(f"in1 = {in1}")
print(f"in2 = {in2}")
print(f"in3 = {in3}")
print(f"in4 = {in4}")
print(f"in5 = {in5}")
print(f"in6 = {in6}")
print(f"in7 = {in7}")
print(f"in8 = {in8}")
print(f"in9 = {in9}")

print(f"out1 = {out1}")
print(f"out2 = {out2}")
print(f"out3 = {out3}")
print(f"out4 = {out4}")
print(f"out5 = {out5}")









