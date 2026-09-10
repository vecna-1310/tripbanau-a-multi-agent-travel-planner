from tools.tavily_tool import tavily_search

from tools.flight_tool import search_flights

# res = tavily_search("Best hotels in India") 
# print(res)

flight_res = search_flights("Plan a 7 days Japan trip from INDIA")
print(flight_res)
