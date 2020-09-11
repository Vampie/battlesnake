class Debug(object):

  @classmethod
  def is_debug_on(cls):
    return True
  
  @classmethod
  def log_with_action(cls, log_string, action_string):
    if cls.is_debug_on():
      print('#### ### ## # ' + action_string)
      print('#### ### ## # ' + log_string)

  @classmethod
  def log(cls, log_string):
    if cls.is_debug_on():
      print('#### ### ## # ' + log_string)
