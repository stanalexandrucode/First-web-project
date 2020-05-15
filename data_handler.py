
import database_common, datetime



@database_common.connection_handler
def get_all_questions(cursor, question_ids):
    print(question_ids)
    print((question_ids,))
    cursor.execute(""" 
            SELECT * FROM question
             WHERE id = %s
             ORDER BY id ASC ; 
      """, ((question_ids,)))

    questions = cursor.fetchall()

    return questions[0]


@database_common.connection_handler
def count_votes(cursor,question_id, number):

    cursor.execute( """  
      UPDATE question
      SET vote_number = vote_number + %s
      WHERE id = %s;
      """, (number, question_id) )


@database_common.connection_handler
def count_votes_for_answers(cursor, answer_id, number):
    cursor.execute("""  
          UPDATE answer
          SET vote_number = vote_number + %s
          WHERE id = %s;
          """, (number, answer_id))

@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
        SELECT * FROM question WHERE id = %s;
    """,(int(question_id),))

    return cursor.fetchone()



@database_common.connection_handler
def delete_question(cursor,question_ids):
    answer = cursor.execute(""" 
        SELECT id FROM answer WHERE question_id = %s;
    """, (question_ids,) )
    answer = cursor.fetchall()

    for answers_ids in answer:
        cursor.execute( """
            DELETE FROM comment WHERE answer_id = %s;
        """, (str(answers_ids['id'])) )
    cursor.execute("""
        DELETE FROM comment WHERE question_id = %s;
    """, (question_ids,))

    cursor.execute("""
                DELETE FROM answer WHERE question_id = %s;
            """, (question_ids,))
    cursor.execute("""
            DELETE FROM question_tag WHERE question_id = %s;
        """, (question_ids,))
    cursor.execute("""
        DELETE FROM question WHERE id = %s;
        """,  (question_ids,) )


@database_common.connection_handler
def count_views(cursor, question_id):
    cursor.execute(f"""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id = %s ;
                   """, (question_id,))


@database_common.connection_handler
def add_new_question(cursor, story):
    cursor.execute("""
        INSERT INTO question (view_number, vote_number,title, message, image, submission_time)
        VALUES (%s,%s, %s,%s, %s, CURRENT_TIMESTAMP);
    """,  (story['view_number'], story['vote_number'], story['title'], story['message'], story['image']) )


@database_common.connection_handler
def add_new_answer(cursor, data):
    cursor.execute("""
        INSERT INTO answer (submission_time, vote_number,question_id,message, image)
        VALUES ( CURRENT_TIMESTAMP,%s, %s, %s, %s );
    """, (data['vote_number'], data['question_id'], data['message'], data['image'])  )


@database_common.connection_handler
def answer_by_question_id(cursor ,question_ids):
    cursor.execute("""
        SELECT * FROM answer WHERE question_id = %s ORDER BY submission_time DESC;
    """, (question_ids,))
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def edit_question(cursor,story):
    cursor.execute("""
        UPDATE question
        SET title = %s, message = %s, image = %s
        WHERE id = %s;
    """, (story['title'], story['message'], story['image'], story['id']) )


@database_common.connection_handler
def sort_by(cursor, criteria='submission_time', order='DESC'):
    if criteria == None or order == None:
        cursor.execute(""" 
                    SELECT * FROM question ORDER BY id ASC ; 
              """)
        questions = cursor.fetchall()

        return questions
    else:
        if order == 'DESC':
            query =f"""SELECT * FROM question ORDER BY {criteria} DESC;"""
        else:
            query =f"""SELECT * FROM question ORDER BY {criteria} ASC;"""
        cursor.execute(query)
        questions = cursor.fetchall()

        return questions