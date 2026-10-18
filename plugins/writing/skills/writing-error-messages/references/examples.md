# Contract illustrations

Wrong: "Oops! Something went wrong."
Right: "The invoice could not be sent. The customer's email address is missing. Add an email on the customer record, then send again."

Wrong: "ERR_VALIDATION_422: invalid_input"
Right (UI): "The start date is after the end date. Choose a start date on or before the end date."
Right (API `message`): "The start date is after the end date. Send `start` less than or equal to `end`."
Right (API metadata): `"code": "DATE_RANGE_INVALID"`

Wrong: a red outline and no text.
Right: the same outline plus the three-part sentence on the field.
