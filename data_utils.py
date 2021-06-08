import DBcm

config = { 
    'host': 'localhost',
    'user': 'polygonuser',
    'password': 'polygonpassword',
    'database': 'polygonreviewsDB',
}

def get_titles_table(orderBy, order):
    with DBcm.UseDatabase(config) as cursor:
        SQL = """select titles.id, titles.name, titles.platform, titles.release_year, titles.genre, titles.studio,
        AVG(IF(reviews.title_id = titles.id, reviews.rating, null)) as "rating",
        Sum(IF(reviews.title_id = titles.id and reviews.liked = 2, 1, 0)) as "likes",
        Sum(IF(reviews.title_id = titles.id and reviews.liked = 1, 1, 0)) as "dislikes",
        Sum(IF(reviews.title_id = titles.id, 1, 0)) as "reviews" from titles,reviews
        group by titles.id
        order by 
        """+orderBy+" "+order
        cursor.execute(SQL)
        titlesData = cursor.fetchall()
    return [ (row) for row in titlesData]

def get_title_info(titleID):
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from titles where titles.id = %s"
        cursor.execute(SQL,(titleID,))
        data = cursor.fetchall()
    return data[0]

def get_reviews(titleID):
    with DBcm.UseDatabase(config) as cursor:
        SQL = """select users.login, reviews.liked, reviews.played, reviews.owned, reviews.rating, reviews.comment 
                from titles, reviews, users 
                where reviews.title_id = titles.id and reviews.user_id = users.id 
                and reviews.title_id = %s"""
        cursor.execute(SQL,(titleID,))
        data = cursor.fetchall()
    return [(row) for row in data]

def get_user_and_password(user, password):
    with DBcm.UseDatabase(config) as cursor:
        SQL = """select * from users where users.login = %s 
        and users.password = %s"""
        cursor.execute(SQL,(user, password))
        data = cursor.fetchall()
    return [(row) for row in data]

def get_user_by_id(userID):
    with DBcm.UseDatabase(config) as cursor:
        SQL = """select users.login from users where users.id = %s"""
        cursor.execute(SQL,(userID,))
        data = cursor.fetchone()
    return data

def get_user(user):
    with DBcm.UseDatabase(config) as cursor:
        SQL = """select * from users where users.login = %s"""
        cursor.execute(SQL,(user,))
        data = cursor.fetchall()
    return [(row) for row in data]

def create_user(user,password):
    with DBcm.UseDatabase(config) as cursor:  
        SQL = "insert into users(login, password) values (%s, %s)"
        cursor.execute(SQL, (user, password))

def create_review(liked, played, owned, rating, comment, titleID, userID):
    with DBcm.UseDatabase(config) as cursor:  
        SQL = """insert into reviews(liked, played, owned, rating, comment, title_id, user_id) 
        values (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(SQL, (liked, played, owned, rating, comment, titleID, userID))

def check_if_title_exists(name, platform):
   with DBcm.UseDatabase(config) as cursor:  
        SQL = """select count(*) from titles where titles.name = %s and titles.platform = %s """
        cursor.execute(SQL, (name, platform))
        titleCount = cursor.fetchone()
        if titleCount[0] >= 1:
            return True
        else:
            return False

def check_if_review_exists(titleID, userID):
   with DBcm.UseDatabase(config) as cursor:  
        SQL = """select count(*) from reviews where reviews.title_id = %s and reviews.user_id = %s"""
        cursor.execute(SQL, (titleID, userID))
        titleCount = cursor.fetchone()
        if titleCount[0] >= 1:
            return True
        else:
            return False

def create_title(name, platform, release_year, genre, studio):
   with DBcm.UseDatabase(config) as cursor:  
        SQL = """insert into titles (name, platform, release_year, genre, studio) 
        values (%s, %s, %s, %s, %s)"""
        cursor.execute(SQL, (name, platform, release_year, genre, studio))