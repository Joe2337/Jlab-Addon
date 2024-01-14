
# Important information:
# The templates are stored per note model, i.e. there may be multiple jlab note types and multiple (different!) instances
# of the jlab templates, each with the same name. This is very good for development, as it enables to create different
# jlab cards (with different fields on the cards / different templates), that are all updated by the addon.
# It could, however, also be a source of errors.
class TemplateNames:
    clozeTemplateName = u"Jlab-ClozeCard"
    listeningTemplateName = u"Jlab-ListeningCard"
    infoTemplateName = u"InfoCard"
    jlabBeginnerTag = "JLAB-B"