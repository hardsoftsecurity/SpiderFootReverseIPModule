# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_reverse_ip_domain
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      David De Maya Merras <daviddemayamerras@gmail.com>
#
# Created:     11/02/2022
# Copyright:   (c) David De Maya Merras 2022
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import requests
import ast

class sfp_reverse_ip_domain(SpiderFootPlugin):

    meta = {
        'name': "Reverse IP Domain",
        'summary': "Module created for the reverse identification of websites hosted on the same IP address.",
        'flags': [""],
        'useCases': ["Custom"],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["IP_ADDRESS"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["DOMAIN_NAME"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            # Insert here the code #
            ########################
            url = f"https://sonar.omnisint.io/reverse/{eventData}"
            peticion = requests.get(url)
            datos = peticion.text
            dominios = ast.literal_eval(datos)
            
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return

        for dominio in dominios:
            evt = SpiderFootEvent("DOMAIN_NAME", dominio, self.__name__, event)
            self.notifyListeners(evt)

# End of sfp_reverse_ip_domain class