import { Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { QuestionComponent } from './question/question.component';

export const routes: Routes = [
  { path: '', redirectTo: '/upload', pathMatch: 'full' },
  { path: 'upload', component: UploadComponent },
  { path: 'question', component: QuestionComponent },
];
