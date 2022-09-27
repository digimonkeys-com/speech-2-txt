import { Component, OnInit} from '@angular/core';
import { UploadService } from '../upload.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  content = ""
  disableBtn = false
  constructor(private service: UploadService) { 
  }

  ngOnInit(): void {
  }

  handleChange = ($event: Event) =>{
    this.content = ($event.target as HTMLInputElement).value
  }

  handleUpload =() =>{
    this.disableBtn = true
    this.service.uploadText(this.content).subscribe( res =>{
      console.log(res), 
      this.disableBtn= false;
      (document.querySelector("#text") as HTMLInputElement).value = ""
    })
  }

}
