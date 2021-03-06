#### RETRIEVING FUNCTIONS 


def extractGroupRelations(groupings, linkages):
    #clean list
    count = 0
    for line in linkages: 
        spl = line.split()
        if len(spl) > 3:
            if '"' in spl[0] and spl[1]:
                newLine=spl[0]+spl[1] + ' '+' '.join(spl[2:])
                linkages[count] = newLine.replace('"', '')
                
            if '"' in spl[-1] and spl[-2]:
                newLine=' '.join(spl[0:2]) + ' ' + spl[-2]+spl[-1] 
                linkages[count] = newLine.replace('"', '')
        count = count +1

    cleaned_linkages = linkages
    # verify if group expends on several lines: create grouping dict
    for group in groupings:

        # extract group name
        groupName = group.split('Group')[1].split('{')[0].strip().replace(' ', '').replace('"', '')
        # extract relations included in grouping
        groupRelations = group.split('Group')[1].split('{')[1].replace('}', '').split()        
        #clean group
        cnt=0
        for elem in groupRelations:
            if (groupRelations[cnt][0] == '"') and (groupRelations[cnt+1][-1]=='"'):
                groupRelations[cnt]=groupRelations[cnt]+groupRelations[cnt+1]
                groupRelations.remove(groupRelations[cnt+1])
            cnt = cnt+1

        # extract relations to duplicate
        toDuplicate = []
        for link in linkages:
            if (groupName in link) and ('-' in link):
                toDuplicate.append(link)
        # extract first and last relations of grouping (ie 'no from' or 'no to' task)
        firstRelation = None
        lastRelation = None
        for elem in groupRelations:
            #print('elem:'+ elem)
            hasFirst = False
            hasLast = False

            for link in linkages:
                #print(link)
                if elem in link.split()[0]:
                    hasLast = True
                    #print('has last')
                elif elem in link.split()[-1]:
                    hasFirst = True
                    #print('has first')

            if not hasFirst:
                firstRelation=elem
            elif not hasLast:
                lastRelation=elem
            else:
                pass

        # regenerate relations according to the type 
        for relation in toDuplicate:
            chunks = relation.split()
            if groupName in chunks:
                if groupName == chunks[0].strip():
                    for elem in groupRelations:
                        #duplicatedRelation = firstRelation + ' ' + ' '.join(chunks[1:])
                        duplicatedRelation =  elem + ' ' + ' '.join(chunks[1:])
                        linkages.append(duplicatedRelation) 
                else: # groupName == chunks[-1].strip():
                    for elem in groupRelations:
                        #duplicatedRelation = firstRelation + ' ' + ' '.join(chunks[1:])
                        duplicatedRelation = ' '.join(chunks[:-1]) + ' ' + elem
                        linkages.append(duplicatedRelation) 
            else:
                pass

        # remove former relations with grouping name
        cleaned_linkages = []
        for relation in linkages:
            if groupName not in relation:
                cleaned_linkages.append(relation)

    return cleaned_linkages


def extractChunks(data):
    events, internalEvents = [], []
    groupings, linkages = [], []
    roles = []
    #misc = []

    for line in data:
        if (line[0] !=  '#'):
            if ('src' in line) and ('tgt' in line):
                lineclean = line.replace('= ', '=').replace(' =', '=').replace(' = ', '=')
                events.append(lineclean)
                for elem in line.split(' '):
                    if ('src' in elem) or ('tgt' in elem):
                        elemclean = elem.strip().replace('tgt=', '').replace('src=', '').replace(']', '')
                        if elemclean != '' and (elemclean not in roles):
                            roles.append(elemclean)
            elif ('-' in line) and ('>' in line):
                linkages.append(line.strip())
            elif ('role=' in line):
                nameChunk = line.split()
                role = nameChunk.pop()
                name=''.join(nameChunk).replace('"', '')
                cleanedInternalEvent = name+' '+ role
                internalEvents.append(cleanedInternalEvent)
            else:
                pass
                #misc.append(line)
            
            for i in range(0, len(linkages)):
                if (linkages[i][0] == '#'):
                    linkages.remove(linkages[i])

    linkages = extractGroupRelations(groupings, linkages)

    chunks = {
        'events':events,
        'internalEvents':internalEvents,
        'linkages':linkages,
    }
    return chunks, roles


def extractRoleChunks(data):
    events, internalEvents = [], []
    linkages = []

    for line in data:
        if (line[0] != '#'): 
            if 'role=' in line:
                internalEvents.append(line)
            elif ('src=' in line) or ('tgt=' in line) or ('?(' in line) or ('!(' in line):
                events.append(line)
            elif ('-' in line) and ('>' in line):
                linkages.append(line)
            else:
                pass
            
    chunks = {
        'events':events,
        'internalEvents':internalEvents,
        'linkages':linkages,
    }
    return chunks



def getLinkages(projRefs, linkages):
    for ref in projRefs:
        testRef=ref.replace('s','').replace('r', '')
        count=0
        for line in linkages:
            if testRef in line:
                lineUpd=line.strip().split(' ')
                i=0
                for elem in lineUpd:
                    if (testRef == elem) and elem[0] != '#':
                        lineUpd[i]=ref
                    i = i+1   
                linkages[count] = ' '.join(lineUpd)
            count = count+1
    #print(linkages)   
    return linkages

    