
def align(japanese, english)
  
  # Turn it into arrays
  j = japanese.split(' ')
  e = english.split(' ')
  
  if (j.length < 3 or e.length < 3)
    # BASE CASE - ONE OF THE TWO ARRAYS IS LENGTH 2 OR LESS
    # -----------------------------------------------------
    if (j.length > 2 or e.length > 2)
      # Case 1: the other one is MORE than 2 -- abort! we can't do anything!
      return nil
    elsif (j.length == e.length)
      # Case 2: they are the same length -- success! return this as an aligned array
      return [japanese, english]
    elsif (j.length == 2 and e.length == 1)
      # Case 3: The japanese is longer than the english. Combine the japanese.
      return [j.join, english]
    elsif (j.length == 1 and e.length == 2)
      # Case 4: The english is longer than that japanese. Split the japanese
      if (japanese.length == 2)
        return ["#{japanese[0,1]} #{japanese[1,1]}", english]
      else
        # we can't split the japanese evenly. abort!
        return nil
      end
    end
    # END BASE CASE
    # -----------------------------------------------------
  else
    # RECURSIVE CASE - BOTH OF THE TWO ARRAYS ARE LENGTH 3 OR GREATER
    # -----------------------------------------------------
    
    # Strategy: Locate the *first* consonant-starting sound in english, then find the appropriate
    # consonant in japanese, then split the problem into two parts
    
    
    
    # END RECURSIVE CASE
    # -----------------------------------------------------    
  end
end


# JAPANESE, ENGLISH, FIXED JAPANESE

def runtest
  test_set = [
    ['KA', 'K AH', 'K A'],
    ['SU', 'SU', 'SU'],
    ['A I', 'AI', 'AI']
  ]
  test_set.each do |test|
    aligned = align(test[0], test[1])
    if (aligned[0] == test[2])
      puts "success - [#{test[0]},#{test[1]}] -> #{test[2]}"
    else
      puts "FAIL!!! - [#{test[0]},#{test[1]}] (output: #{aligned})"
    end
  end

end

# -- MAIN --


# filename = "test.txt" #ARGV[0]
# split = align('KA', 'K AH')
# puts split

runtest

# File.open(filename).each { |line|
#   puts ">> #{line}"
#   parts = line.split(',')
#   align(parts[2], parts[3])  
# }