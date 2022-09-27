import { Component, OnInit } from '@angular/core';
import { StatusService } from '../status.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit {

  constructor(private service:StatusService) { 
    service.getStatus().subscribe(res =>{
      this.totalDuration = res.duration
      this.recorded = res.recorded_samples
      this.toRecord = res.unrecorded_samples
      this.percentage = (res.recorded_samples / res.samples) * 100
      this.total = res.samples
    })
  }

  totalDuration = 0
  recorded = 0
  toRecord = 0
  percentage = 100
  total = 0

  ngOnInit(): void {
  }

  floor(num: number){
    return Math.floor(num)
  }

}
