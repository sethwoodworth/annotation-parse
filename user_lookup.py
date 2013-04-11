import FCUtil

class UserLookup(object):

	def __init__(self):
		super(UserLookup,self).__init__()
		self.users = FCUtil.openJsonFile('users.json')

	def getUserName(self,id):
		try:
			return self.users[str(id)]['username'].strip().strip('\'')
		except:
			print 'No User '+str(id)
			return None