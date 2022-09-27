import { Component, AfterContentInit } from '@angular/core';
import { detectBrowserName } from 'src/app/utils';
import { RecordService } from '../record.service';
import fixWebmDuration from "fix-webm-duration";
import { HostListener } from '@angular/core';

@Component({
  selector: 'app-record',
  templateUrl: './record.component.html',
  styleUrls: ['./record.component.scss']
})
export class RecordComponent implements AfterContentInit {

  browser = ""
  text = ""
  textId = -1
  isRecording = false
  isUploading = false
  mediaRecorder:  MediaRecorder = new MediaRecorder(new MediaStream())
  audioUrl =  ""
  audioBlob = new Blob()
  audioChunks:BlobPart[] = [];
  startTime = 0
  duration = 0
  showInfo = true

  initRecorder =() =>{
    navigator.mediaDevices.getUserMedia({ audio: true, video:false })
    .then(stream => {
      if (this.browser=="firefox"){
        this.mediaRecorder = new MediaRecorder(stream, {mimeType:'audio/ogg;codecs=opus'});
      } else {
        this.mediaRecorder = new MediaRecorder(stream, {mimeType:'audio/webm;codecs=opus'});
      }

      this.mediaRecorder.addEventListener("dataavailable", event => {
        let data = event.data;
        if (data && data.size > 0) {
          this.audioChunks.push(event.data);
        }
      });

      this.mediaRecorder.addEventListener("stop", () => {
        this.duration = Date.now() - this.startTime;
        this.audioBlob = new Blob(this.audioChunks, {type: this.mediaRecorder.mimeType.toString()});
        this.audioUrl = URL.createObjectURL(this.audioBlob);
        this.isRecording = false
      });
    });
  }

  constructor(private service: RecordService) {
    this.browser = detectBrowserName()
    service.getText().subscribe(res =>{
      this.textId = res.samples[0].id
      this.text = res.samples[0].transcription
    })

    
  }
  ngAfterContentInit(): void {
    this.initRecorder()
  }

  recordAudio =()=>{
    this.isRecording = true
    this.mediaRecorder.start()
    this.startTime = Date.now();
  }

  stopRecording = () =>{
    this.mediaRecorder.stop()
  }
  playAudio = () =>{
    const audio = new Audio(this.audioUrl)
    audio.play()
  }

  clear =() =>{
    this.audioUrl =  ""
    this.audioBlob = new Blob()
    this.audioChunks = [];
    this.duration = 0
    this. startTime = 0
  }

  submitSample = async () =>{
    this.isUploading = true
    let blob = this.audioBlob
    if (this.browser == "chrome") {
      blob = await fixWebmDuration(blob, this.duration)
    }
    this.service.uploadRecording(this.textId, blob, this.browser).subscribe(res =>{
      console.log(res.info)
      this.service.getText().subscribe(res =>{
        this.textId = res.samples[0].id
        this.text = res.samples[0].transcription
        this.isUploading = false
        this.clear()
      })
      
      
    })
  }

  hideInfo = () =>{
    this.showInfo = false
  }

  deleteSample = () => {
    this. isUploading =true
    this.service.deleteSample(this.textId).subscribe(res =>{
      console.log(res.info)
      this.service.getText().subscribe(res =>{
        this.textId = res.samples[0].id
        this.text = res.samples[0].transcription
        this.isUploading = false
        this.clear()
    })
  })


}

@HostListener('document:keypress', ['$event'])
handleKeyboardEvent(event: KeyboardEvent) { 
  if (event.key === "q"){
    this.recordAudio()
  } else if (event.key === "w"){
    this.stopRecording()
  } else if (event.key === "e"){
    this.playAudio()
  }
}

}
