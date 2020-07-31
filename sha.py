import sys



class operators():
    def truncate(data,leng):

        while (len(data) > leng):
            data = data[1:]

        return data

    def _xor(a_a,b_b):
        return_string = ""
        for x_a,x_b in zip(a_a,b_b):
            if x_a == x_b:
                return_string += '0'
            else:
                return_string += '1'
        return return_string
    def _and(a_a,b_b):
        return_string = ""
        for x_a,x_b in zip(a_a,b_b):
            if x_a == '1' and x_b == '1':
                return_string += '1'
            elif x_a == '0' and x_b == '0':
                return_string += '0'
            elif x_a == '1' and x_b == '0':
                return_string += '0'
            if x_a == '0' and x_b == '1':
                return_string += '0'
        return return_string
    def _or(a_a,b_b):
        return_string = ""
        for x_a,x_b in zip(a_a,b_b):
            if x_a == '1' and x_b == '0':
                return_string+='1'
            if x_a == '0' and x_b == '1':
                return_string+='1'
            if x_a == '1' and x_b == '1':
                return_string+='1'
            if x_a == '0' and x_b == '0':
                return_string+='0'
        return return_string
    def _not(a_a):
        return_string=""
        for x_a in a_a:
            if x_a =='1':
                return_string+='0'
            else:
                return_string+='1'
        return return_string
    def left_rotate(n,nl):
        return n[nl:] + n[:nl]
class SHA_CLASS(operators):
    def __init__(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-f','--file',help='add -f file.txt\nto calculate the hash of that file\neg. sha.py -f file.txt')
        parser.add_argument('-s','--string')

        args = parser.parse_args()
        if args.file:
            #print(args.file)
            file_hash = open(args.file,'r')
            self.input_string = file_hash.read()
            #print(self.input_string)
            file_hash.close()
        elif args.string:
            self.input_string = args.string
        ascii_list = []
        self.binary_list = []
        for x in self.input_string:
            self.binary_list.append(format(ord(x),'08b'))

    def padding(self): #problem with padding of string doesn't accept more than 56 char

        self.binary_string = ''.join(self.binary_list)
        chunk_no = len(self.binary_string) % 512
        #print(chunk_no)
        self.binary_string = self.binary_string +'1'
        for i in range(chunk_no+1,448):
            self.binary_string+='0'
        ml = format(len(self.binary_list)*8,'064b')
        self.padded_string = self.binary_string+ml
        #print(len(self.padded_string))
        self.chunk_of_512 = list(map(''.join,zip(*[iter(self.padded_string)]*512)))
        #print(len(self.chunk_of_512[0]))
    def divide_into_16(self):

        self.h0 = '01100111010001010010001100000001'
        self.h1 = '11101111110011011010101110001001'
        self.h2 = '10011000101110101101110011111110'
        self.h3 = '00010000001100100101010001110110'
        self.h4 = '11000011110100101110000111110000'


        for chunk_iter in self.chunk_of_512:

            a = self.h0
            b = self.h1
            c = self.h2
            d = self.h3
            e = self.h4
            w = list(map(''.join,zip(*[iter(chunk_iter)]*32)))

            f_f_f = '11111111111111111111111111111111'

            for i in range(16, 80):
                w.append("") #causes indexError if removed so like you know don't remove!
                w[i] = operators.left_rotate(operators._xor(operators._xor(operators._xor(w[i - 3] , w[i - 8]) , w[i - 14]) , w[i - 16]), 1)

            for i in range(0,80):
                #print(i)
                if 0 <= i <=19:
                    #f = operators._xor(d,operators._and(b,operators._xor(c,d)))
                    f = operators._or(operators._and(b,c),operators._and(operators._not(b),d))
                    k = '1011010100000100111100110011001'
                if 20 <= i <=39:
                    f = operators._xor(b,operators._xor(c,d))
                    k = '1101110110110011110101110100001'
                    #print(i)
                if 40 <= i <=59:
                    f = operators._or(operators._and(b,c),operators._or(operators._and(b,d),operators._and(c,d)))
                    k = '10001111000110111011110011011100'

                if 60 <= i <= 79:
                    f = operators._xor(b,operators._xor(c,d))
                    k = '11001010011000101100000111010110'

                temp = int(operators.left_rotate(a,5),2) + int(f,2) + int(e,2) + int(k,2) + int(w[i],2)
                temp = str(bin(temp)[2:])
                temp = operators.truncate(temp,32)
                b,c,d,e=(a,operators.left_rotate(b,30),c,d)
                a = temp


            self.h0 = operators.truncate(bin(int(self.h0,2) + int(a,2))[2:],32)
            self.h1 = operators.truncate(bin(int(self.h1,2) + int(b,2))[2:],32)
            self.h2 = operators.truncate(bin(int(self.h2,2) + int(c,2))[2:],32)
            self.h3 = operators.truncate(bin(int(self.h3,2) + int(d,2))[2:],32)
            self.h4 = operators.truncate(bin(int(self.h4,2) + int(e,2))[2:],32)

        hh = hex(int(self.h0,2))[2:] + hex(int(self.h1,2))[2:] + hex(int(self.h2,2))[2:] + hex(int(self.h3,2))[2:]+ hex(int(self.h4,2))[2:]
        print(hh)


o = SHA_CLASS()
o.padding()
o.divide_into_16()
