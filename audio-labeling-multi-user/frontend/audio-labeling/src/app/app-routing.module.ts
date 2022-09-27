import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecordComponent } from './recording/record/record.component';
import { StatusComponent } from './status/status/status.component';
import { UploadComponent } from './text-upload/upload/upload.component';

const routes: Routes = [
  {path: 'upload-text', component:  UploadComponent},
  {path: 'record', component:  RecordComponent},
  {path:'', component: StatusComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
