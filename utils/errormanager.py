def standardized_error(error_msg, additional_info = ""):
    return '🚨 | **Error:** `{}`\n{}'.format(error_msg, ("" if additional_info == "" else "🔸 | {}".format(additional_info)))