from instagram_scraper.model.insta import User, Post, Comment

def create_user(name="",i_handle=""):
	if name or i_handle:
		try:
			ob=User(username=name,handle=i_handle)
			ob.save()
			return ob
		except Exception as error:
			print("Error Occured while Creating User \n",error)

def create_post(name="",caption="",u_id=None):
	if name or caption:
		try:
			ob=Post(img_name=name,caption=caption,user_id=u_id)
			ob.save()
			return ob
		except Exception as error:
			print("Error occured while creating a new Post \n",error)

def create_comment(name="",text="",p_id=None):
	if name or text:
		try:
			ob=Comment(user=name,text=text,post_id=p_id)
			ob.save()
			return ob
		except Exception as error:
			print("Error occured while creating a Comment \n",error)
