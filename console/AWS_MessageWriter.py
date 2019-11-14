class messageSection:
    '''holds messages to be placed into reports and emails
        arg: messageHeader = Title of the message
        
        Properties:
            header: sets/returns messageHeader
            description: sets/returns a description of information in section
            message: sets/returns a message to be placed in section
    '''
    
    def __init__(self, messageHeader: str, description: str='', message: str='', footer: str=''):
        self.headerText = messageHeader
        self.descriptionText = description
        self.messageText = message
        self.footerText = footer
    
    @property
    def header(self)->str:
        return self.headerText
    
    @header.setter
    def header(self, headerText: str):
        '''sets header text for message'''
        self.headerText = headerText
    
     
    @property
    def description(self)->str:
        return self.descriptionText
    
    @description.setter
    def description(self, descriptionText: str):
        self.descriptionText = descriptionText
        
    
    @property
    def message(self)->str:
        return self.messageText
    
    @message.setter
    def message(self, messageText: str):
        self.messageText = messageText

    @property
    def footer(self)->str:
        return self.messageText
    
    @footer.setter
    def footer(self, footerText: str):
        self.footerText = footerText

    def __str__(self):
        retStr = f'''<h2>{self.headerText}<h2><br><br>\n
        <p>{self.descriptionText}</p><br><br>\n
        {self.messageText}<br><br>\n{self.footerText}'''
        
        return retStr



