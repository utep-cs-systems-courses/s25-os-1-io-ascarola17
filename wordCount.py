import os
import sys
import re

def read_file(input_file):
    try:
        #Open the file 
        fd = os.open(input_file, os.O_RDONLY)
        #Create an empty byte string bc we are using os.read 
        content = b""

        while True:
            #Read in chunks of 1024 bytes, read() only returns raw bytes
            chunk = os.read(fd, 1024)  
            if not chunk:
                #we reached the end of file
                break  
            #append to content
            content += chunk  
        #Close file
        os.close(fd)  
        #Convert bytes to string
        return content.decode()  
    #Catch any errors 
    except OSError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)    

#Method to count the occurence of each word
def count_words(text):
    #Ignore cases
    text = text.lower()
    #pattern, replace, text 
    #Removes anything that isnt a letter or number
    text = re.sub(r"[^\w\s]", "", text)

    #splits text into words
    words = text.split()

    #Create dictonaries 
    word_count = {}
    #Go through all the words
    for word in words:
        #counts each word and puts it into the dictonary 
        word_count[word] = word_count.get(word,0) + 1
    #return the word count
    return word_count

#Method to sort the words alphabetically
def sort_word_counts(word_count):
    #Sort alphabetically
    return sorted(word_count.items(), key=lambda x: x[0])  

#Method to write on the output file
def write_output(output_file, sorted_word_counts):
    try:
        # Open file (path, flags, mode), flags: open file for writing/ create if not existent / Empty file if exist
        #0o644 = File owner can read and write 
        fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

        #Write each word and count into the file
        for word, count in sorted_word_counts:
            line = f"{word} {count}\n"
            #Convert string to bytes and write
            os.write(fd, line.encode())  
        #Close the file when done 
        os.close(fd)
        #Print output message to confirm it worked
        print(f"Successfully wrote word counts to {output_file}")
    #Error message 
    except OSError as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    #Make sure corret thing is passed into terminal 
    if len(sys.argv) != 3:
        print("Usage: python wordCount.py input.txt output.txt")
        sys.exit(1)
    #To know what files to read/write without having to deal w file names
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    #Read the file
    text = read_file(input_file)  
    #Print content for debugging/testing
    #print("File Content:\n", text)  

    #Count words
    word_counts = count_words(text)  
    # Sort alphabetically
    sorted_word_counts = sort_word_counts(word_counts)

    #Write sorted words to output file
    write_output(output_file, sorted_word_counts) 
