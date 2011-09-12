def getTags(elements):
	tags = []
	for e in elements:
		tags.append(e.tag)
	return tags

def checkType(elem, elemtype, schema):
	taglist = getTags(elem)
	requiredList = schema[elemtype]["requireds"]
	for k in range(len(requiredList)):
		if not(requiredList[k] in taglist):
			return False
	return True

def fullrequiredCheck(root, schema, fname):
	
	print "Running full check on required xml fields"
	ferr = open(fname + "fullerrors.err","w")

	for vipelem in root:
		ident = vipelem.get("id")
		if schema["vip_object"][vipelem.tag]["indicator"] == "all":
			children = vipelem.getchildren()
			childrenTags = getTags(children)
			requiredList = schema["vip_object"][vipelem.tag]["requireds"]
			elements = schema["vip_object"][vipelem.tag]["elements"]
			for element in requiredList:
				if not element in childrenTags:
					ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing " + element + "\n")
				elif element in schema and schema[element]["type"] == "complexType":#check here for the type, if the type is valid in complex type from the schema, continue searching for required elements
			for i in range(len(elements)):
				if elements[i]["name"] in requiredList:
					if not(elements[i]["name"] in childrenTags):
						ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing " + elements[i]["name"] + "\n")
					elif elements[i]["type"][0:3] != "xs:" and schema[elements[i]["type"]]["type"] == "complexType":
						for c in children:
							if element[i]["name"] == c.tag:
								if not(checkType(c,elements[i]["type"],schema)):
									ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing field in '" + elements[i]["name"] + "'\n")
								break
		else:
			children = vipelem.getchildren()
			j = 0
			for i in range(len(schema["vip_object"][vipelem.tag]["elements"])):
				if j >= len(children):
					if schema["vip_object"][vipelem.tag]["elements"][i]["required"] == "True":
						ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing " + schema["vip_object"][vipelem.tag]["elements"][i]["name"]+"\n")
						break 
				elif schema["vip_object"][vipelem.tag]["elements"][i]["name"] == children[j].tag:
					if schema["vip_object"][vipelem.tag]["elements"][i]["type"][0:3] != "xs:":
						if not(checkType(children[j],schema["vip_object"][vipelem.tag]["elements"][i]["type"][0:3])):
							ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing field in '" + schema["vip_object"][vipelem.tag]["elements"][i]["name"] + "'\n")
							break
					j+=1
				elif schema["vip_object"][vipelem.tag]["elements"][i]["required"] == "True":
					ferr.write("Error '" + vipelem.tag + "' ID:" + str(ident) + " missing " + schema["vip_object"][vipelem.tag]["elements"][i]["name"] + "\n")
					break
	print "Finished full required xml field check, data located in " + fname + "fullerrors.err"
	ferr.close()