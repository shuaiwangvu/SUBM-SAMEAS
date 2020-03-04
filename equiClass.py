# this is a part of SUBMASSIVE and it manages the sameas class with data from Joe

import csv

# file_name = "term2id.csv"
# file_name = "term2id_0-99_1000.csv"
file_name = "./sameAs/term2id_0-99.csv"

def splitTermAndID(line):
    parts = line.split(" ")
    if len(parts) ==2:
        return parts
    else:
        # when an element contains an empty space
        term = ""
        for i in range(len(parts) - 1):
            term = term + parts[i]
        return [term, parts[-1]]

class equiClassManager:

    def __init__(self, path):
        # define a path to the equivalent class
        self.file_path = path
        # self.index_to_list = {}
        self.class_name_to_index = {}

        with open(file_name) as f:
            line = f.readline()
            if (line == 'TERM,GROUPID\n'):
                line = f.readline()
            cnt = 0
            while line:

                splitted_line = splitTermAndID(line)
                # values
                num = int(splitted_line[1])
                # key
                class_name_string = splitted_line[0]
                # if '^^' in class_name_string:
                #     class_name_string = class_name_string.split('^^')
                #     class_name_string = str(class_name_string[0][1:-1])

                # print(line)
                # print('name:', class_name_string, '\nindex:', num, '\n')

                # print ('type',type(class_name_string))
                self.class_name_to_index[class_name_string] = num
                #
                # if class_name_string in self.class_name_to_index.keys():
                #     self.class_name_to_index[class_name_string].append(num)
                # else:
                #     self.class_name_to_index[class_name_string] = [num]
                # print (self.class_name_to_index)
                # if (num in self.index_to_list.keys()):
                #     self.index_to_list[num].append(class_name_string)
                # else:
                #     self.index_to_list[num] = [class_name_string]
                # print ('index to list = ', self.index_to_list[num])
                # print(class_name_string, num)
                line = f.readline()
                cnt += 1
                if (cnt%10000000 == 0):
                    print (cnt)

        # for c in self.class_name_to_index.keys():
        #     if len(self.class_name_to_index[c]) != 1:
        #         print ('IN MULTIPLE EQUIVALENT CLASSES: ', c, '\n',self.class_name_to_index[c])
        # print ('There are in total {:,} groups'.format(len(self.index_to_list.keys())))
        # # print (self.class_name_to_index.keys())
        # print ('There are in total {:,} classes'.format(len(self.class_name_to_index.keys())))
            # print("DONE! Finished reading file TERM2ID. There is a total of ", "{:,}".format(cnt), "terms")

    def find_index (self, t):
        if t in self.class_name_to_index.keys():
            return 10000000 + self.class_name_to_index[t]
        else:
            return None

    def test_equivalent (self, t1, t2):
        # t1_indeces = []
        # t2_indeces = []
        # if t1 in self.class_name_to_index.keys():
        #      t1_indeces = self.class_name_to_index[t1]
        # if t2 in self.class_name_to_index.keys():
        #      t2_indeces = self.class_name_to_index[t2]
        # l = [value for value in t1_indeces if value in t2_indeces]
        if t1 in self.class_name_to_index.keys() and t2 in self.class_name_to_index.keys():
            return (self.class_name_to_index[t1] == self.class_name_to_index[t2])
            return
        else:
            return False

if __name__ == "__main__":
    e = equiClassManager(file_name)
    # for i in range(100):
    #     k = list(e.index_to_list.keys())[i]
    #     print ('for group index ', k, ' its members are: ', e.index_to_list[k])
    #     for m in  e.index_to_list[k]:
    #         print ('the index is ', e.class_name_to_index[m])
