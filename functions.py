from .statics import notes,scales,chords

def show(kind):
    if kind=='notes':
        return list(notes.keys())
    elif kind=='scales':
        return list(scales.keys())
    elif kind=='chords':
        return list(chords.keys())
    else:
        return 'input should be \'notes\',\'scales\' or \'chords\''

#Input example do_scale('B','Phrygian')
#Output example ['B', 'C', 'D', 'E', 'F#', 'G', 'A']
def form_scale(note,scale): 
    result=[note,]

    for j in [(x+notes[note][0])%12 for x in scales[scale]]:
        for i in list(notes.keys()):
            if notes[i][0]==j:
                result.append(i)

    return tuple(result)

#input example ('A','mayor')
#output example ('A', 'C#', 'E')
def form_chord(note,chord):
    result=[]

    for j in [(x+notes[note][0])%12 for x in chords[chord]]:
        for i in list(notes.keys()):
            if notes[i][0]==j:
                result.append(i)
    return tuple(result)


#input:['A','B','C#'] or ('A',['C#','F'],('A','B','C#'))
#list of scales on which the notes are whitin, more if first_note_on_scale is '', less but whit first note on the scale equal to first_note_on_scale
#if first_note is set and desired_scale is set the result is True or False
def belong_scale(notes_list,first_note_on_scale='',desired_scale=''):
    def types_list(iter):
        if all(list(map(lambda item:isinstance(item,str),iter))):
            return 'str'
        else:
            return 'other'

    summ=[]
    if types_list(notes_list)=='other':
        for item in notes_list:
            summ=summ+list(item)

    if len(summ)>0:
        notes_list=summ
    
    if first_note_on_scale=='':
        result=[]
        for note in list(notes.keys()):
            for scale in list(scales.keys()):
                if all(list(map(lambda item: True if item in form_scale(note,scale) else False,notes_list)))==True:
                    result.append((note+' '+scale,form_scale(note,scale)))
        return result
    else:
        if desired_scale=='':
            result=[]        
            for scale in list(scales.keys()):
                if all(list(map(lambda item: True if item in form_scale(first_note_on_scale,scale) else False,notes_list)))==True:
                    result.append((first_note_on_scale+' '+scale,form_scale(first_note_on_scale,scale)))
            return result
        else:
            scale=form_scale(first_note_on_scale,desired_scale)
            if all(list(map(lambda item: True if item in scale else False,notes_list)))==True:
                return True
            else:
                return False



def which_chord(notes_list,first_note='',ordered=False,exact_length=False):
    if first_note not in notes_list and first_note!='':
        return print('First note should be in the notes list')

    result=[]
    for note in list(notes.keys()):
        for chord in list(chords.keys()):
            if all(list(map(lambda item: True if item in form_chord(note,chord) else False,notes_list)))==True:
                result.append((note+' '+chord,form_chord(note,chord)))

    
    if first_note=='':
        if ordered==False:
            if exact_length==False:
                return result
            else:
                result=list(x for x in result if len(x[1])==len(notes_list))
                return result
        else:
            def right_order(base_list,new_list):
                for i in range(len(base_list)-1):
                    if new_list.index(base_list[i+1]) - new_list.index(base_list[i])<0:
                        return False
                return True

            result=list(x for x in result if right_order(notes_list,x[1]))            
            if exact_length==False:
                return result
            else:
                result=list(x for x in result if len(x[1])==len(notes_list))
                return result
    else:
        result=list(x for x in result if first_note==x[1][0])
        if ordered==False:
            if exact_length==False:
                return result
            else:
                result=list(x for x in result if len(x[1])==len(notes_list))
                return result
        else:
            def right_order(base_list,new_list):
                for i in range(len(base_list)-1):
                    if new_list.index(base_list[i+1]) - new_list.index(base_list[i])<0:
                        return False
                return True

            result=list(x for x in result if right_order(notes_list,x[1]))            
            if exact_length==False:
                return result
            else:
                result=list(x for x in result if len(x[1])==len(notes_list))
                return result



def chords_in_scale(scale_note,desired_scale,min_len=2,max_len=6):
    if min_len<2 or max_len>6:
        print('min length is 2 and max length is 6')
    result=[]
    for note in form_scale(scale_note,desired_scale):
        for chord in list(chords.keys()):
            actual_chord=form_chord(note,chord)
            if belong_scale(actual_chord,scale_note,desired_scale) and len(actual_chord)>=min_len and len(actual_chord)<=max_len:
                result.append((note+' '+chord,actual_chord))
    return result
