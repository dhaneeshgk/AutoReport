from dbs import dbs



def validate_headers(headers,validate_token=True,validate_content_type=True):
    try:
        if validate_content_type:
            if not "Content-Type" in headers:
                return {"status":False,"remarks":"please contact adminstrator"}
            elif not headers["Content-Type"] == "application/json":
                return {"status":False,"remarks":"please contact adminstrator"}
            elif not validate_token:
                return {"status":True,"remarks":"headers validated"}

        if validate_token:
            if "Authorization" in headers:
                # query = conn.execute("select * from users where access_token='{access_token}'".format(access_token=access_token))
                d_s = dbs.get_row("users",which_="all",where_={"access_token":headers["Authorization"]})
                # print("d_s",d_s)
                q_c = list(d_s["values"])
                if q_c:
                    details = list(q_c[0])
                    return {"status":True,"email":details[0],"access_token":details[1]}
                else:
                    return {"status":False,"remarks":"Invalid access token"}
            else:
                return {"status":False,"remarks":"please provide access token"}
    except Exception as e:
        return {"status":False,"remarks":str(e)}
