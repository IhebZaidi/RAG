import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './upload/upload.component'; // Importer le composant Upload
import { QuestionComponent } from './question/question.component'; // Importer le composant Question

@Component({
  selector: 'app-root',
  standalone: true, // Indiquer que ce composant est autonome
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [CommonModule, QuestionComponent], // Ajouter les composants Importés ici
})
export class AppComponent {
  title = 'Application de Gestion des CV et Chat IA';
}
