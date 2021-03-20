from pyudemy import Udemy

client = Udemy("Z4iHcLBb8gtAv1lKRnW7fley2jwqkb9Ws6yBDd9x", "wjkd2mWGAhU9A2lIMVrHhMVOdB5Wz9QOtyFfhBQVrD5EcLVjNEGpdiEIQD4PNuuX1d7pprgbdtugtQmUwExLQzudkZxRDvTDPpAC6kYlOPMizrcVq9JyLJXQRXTotBvO")
course = client.courses(page=1, page_size=5, search='machine learning')
course_detail = client.course_detail(id='1968412')
course_review = client.course_reviews('950390')

for review in course_review['results']:
    print(review['content'])