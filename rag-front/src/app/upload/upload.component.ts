import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Importer CommonModule
import axios from 'axios';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css'],
  standalone: true, // Indiquer que le composant est autonome
  imports: [CommonModule], // Ajouter CommonModule dans les imports
})
export class UploadComponent {
  selectedFile: File | null = null;
  loading: boolean = false;
  message: string = '';

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      if (file.type === 'application/pdf') {
        this.selectedFile = file;
        this.message = `Fichier sélectionné : ${file.name}`;
      } else {
        this.selectedFile = null;
        this.message = 'Veuillez sélectionner un fichier PDF.';
      }
    }
  }

  async uploadFile() {
    if (!this.selectedFile) {
      alert('Veuillez sélectionner un fichier.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.loading = true;
    this.message = 'Téléchargement en cours...';

    try {
      const response = await axios.post('http://localhost:8000/upload/', formData);
      this.message = 'Fichier envoyé avec succès!';
      alert('Fichier envoyé avec succès!');
    } catch (error) {
      this.message = 'Erreur lors de l\'envoi du fichier.';
      alert('Erreur lors de l\'envoi du fichier.');
    } finally {
      this.loading = false;
    }
  }
}
 