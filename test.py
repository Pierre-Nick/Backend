from packages.Job.util import replace_commas_with_semicolons

data = "[85; \'051000012616\'; \"CAMPBELL\'S CREAM OF MUSHROOiM SOUP\", "
data = replace_commas_with_semicolons(data)
print(data)
