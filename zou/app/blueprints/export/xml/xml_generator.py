import xml.etree.ElementTree as ET

def create_xml_timeline(timeline_name, fps, clip_items):
    # Create root element
    xmeml = ET.Element('xmeml', version='5')

    # Create sequence element
    sequence = ET.SubElement(xmeml, 'sequence')
    
    # Add timeline name
    name = ET.SubElement(sequence, 'name')
    name.text = timeline_name
    
    # Add duration placeholder (will be calculated)
    total_duration = sum(clip['duration'] for clip in clip_items)
    duration = ET.SubElement(sequence, 'duration')
    duration.text = str(total_duration)
    
    # Add rate element
    rate = ET.SubElement(sequence, 'rate')
    timebase = ET.SubElement(rate, 'timebase')
    timebase.text = str(fps)
    ntsc = ET.SubElement(rate, 'ntsc')
    ntsc.text = 'FALSE'
    ET.SubElement(sequence, "in").text = '-1'
    ET.SubElement(sequence, "out").text = '-1'
    
    # Add timecode element
    timecode = ET.SubElement(sequence, 'timecode')
    timecode_string = ET.SubElement(timecode, 'string')
    timecode_string.text = "01:00:00:00"
    timecode_frame = ET.SubElement(timecode, 'frame')
    timecode_frame.text = str(int(fps) * 3600)  # Example for 1-hour start time
    displayformat = ET.SubElement(timecode, 'displayformat')
    displayformat.text = 'NDF'
    timecode_rate = ET.SubElement(timecode, 'rate')
    timecode_timebase = ET.SubElement(timecode_rate, 'timebase')
    timecode_timebase.text = str(fps)
    timecode_ntsc = ET.SubElement(timecode_rate, 'ntsc')
    timecode_ntsc.text = 'FALSE'
    
    # Add media element
    media = ET.SubElement(sequence, 'media')
    video = ET.SubElement(media, 'video')
    
    # Create video track
    track = ET.SubElement(video, 'track')


    last_duration = 0
    for index, clip in enumerate(clip_items):
        clipitem = ET.SubElement(track, 'clipitem', id=f"{clip['name']} {index}")
        
        # Clip name
        clip_name = ET.SubElement(clipitem, 'name')
        clip_name.text = clip['name']
        
        # Duration
        clip_duration = ET.SubElement(clipitem, 'duration')
        clip_duration.text = str(clip['duration'])
        
        # Clip rate
        clip_rate = ET.SubElement(clipitem, 'rate')
        clip_timebase = ET.SubElement(clip_rate, 'timebase')
        clip_timebase.text = str(fps)
        clip_ntsc = ET.SubElement(clip_rate, 'ntsc')
        clip_ntsc.text = 'FALSE'
        
        # Start and end time
        start = ET.SubElement(clipitem, 'start')
        start.text = str(last_duration)
        end = ET.SubElement(clipitem, 'end')
        end.text = str(clip['duration']+last_duration)

        ET.SubElement(clipitem, 'enabled').text = 'TRUE'
        
        # In and out points
        clip_in = ET.SubElement(clipitem, 'in')
        clip_in.text = str(0)
        clip_out = ET.SubElement(clipitem, 'out')
        clip_out.text = str(clip['duration'])
        
        # File reference
        file = ET.SubElement(clipitem, 'file', id=f"{clip['name']} {index + 2}")
        
        # File duration
        file_duration = ET.SubElement(file, 'duration')
        file_duration.text = str(clip['duration'])

        # File rate
        file_rate = ET.SubElement(file, 'rate')
        file_timebase = ET.SubElement(file_rate, 'timebase')
        file_timebase.text = str(fps)
        file_ntsc = ET.SubElement(file_rate, 'ntsc')
        file_ntsc.text = 'FALSE'

        file_name = ET.SubElement(file, 'name')
        file_name.text = clip['name']
        file_pathurl = ET.SubElement(file, 'pathurl')
        file_pathurl.text = clip['pathurl']

        # Add timecode element
        timecode = ET.SubElement(file, 'timecode')
        timecode_string = ET.SubElement(timecode, 'string')
        timecode_string.text = "00:00:00:00"
        displayformat = ET.SubElement(timecode, 'displayformat')
        displayformat.text = 'NDF'
        timecode_rate = ET.SubElement(timecode, 'rate')
        timecode_timebase = ET.SubElement(timecode_rate, 'timebase')
        timecode_timebase.text = str(fps)
        timecode_ntsc = ET.SubElement(timecode_rate, 'ntsc')
        timecode_ntsc.text = 'FALSE'
        
        # Video media info
        file_media = ET.SubElement(file, 'media')
        file_video = ET.SubElement(file_media, 'video')
        file_video_duration = ET.SubElement(file_video, 'duration')
        file_video_duration.text = str(clip['duration'])
        
        # Video characteristics
        sample_characteristics = ET.SubElement(file_video, 'samplecharacteristics')
        width = ET.SubElement(sample_characteristics, 'width')
        width.text = str(clip['width'])
        height = ET.SubElement(sample_characteristics, 'height')
        height.text = str(clip['height'])
        
        # Composite mode
        composite_mode = ET.SubElement(clipitem, 'compositemode')
        composite_mode.text = 'normal'

        last_duration = clip['duration']
        
    format_ = ET.SubElement(video, "format")
    samplecharacteristics = ET.SubElement(format_, "samplecharacteristics")
    ET.SubElement(samplecharacteristics, "width").text = str(clip['width'])
    ET.SubElement(samplecharacteristics, "height").text = str(clip['height'])
    ET.SubElement(samplecharacteristics, "pixelaspectratio").text = "square"
    formate_rate = ET.SubElement(samplecharacteristics, "rate")
    formate_timebase = ET.SubElement(formate_rate, 'timebase')
    formate_timebase.text = str(fps)
    formate_ntsc = ET.SubElement(formate_rate, 'ntsc')
    formate_ntsc.text = 'FALSE'
        
    # Convert to string
    xml_str = ET.tostring(xmeml, encoding='UTF-8', method='xml')
    return xml_str.decode('UTF-8')

if __name__ == '__main__':
        
    # Example usage
    timeline_name = "TimelineName (Resolve)"
    fps = 24
    clip_items = [
        {
            'name': 'linear.mp4',
            'duration': 7,
            'pathurl': 'file://localhost/E:/test/linear.mp4',
            'width': 1920,
            'height': 1080,
        },
        {
            'name': 'linear.mov',
            'duration': 7,
            'pathurl': 'file://localhost/E:/test/linear.mov',
            'width': 1920,
            'height': 1080,
        }   
    ]

    xml_timeline = create_xml_timeline(timeline_name, fps, clip_items)
    print(xml_timeline)
