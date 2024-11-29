import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';


@Component({
  selector: 'app-question',
  standalone: true,
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css'],
  imports: [CommonModule, FormsModule],
})


export class QuestionComponent {
  question: string = '';
  file: File | null = null;
  answer: string = '';
  messages: { content: string, sender: string }[] = [];
  loading: boolean = false;
  fileUrl: string | null = null;

  constructor(private apiService: ApiService) {}
  // Gérer le changement de fichier
  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input?.files?.[0]) {
      const file = input.files[0];
      if (file.type !== 'application/pdf') {
        alert('Seul un fichier PDF est autorisé.');
        this.file = null;
      } else {
        this.file = file;
        this.fileUrl = URL.createObjectURL(file);  // Créer une URL pour le fichier
        console.log('Fichier sélectionné:', file.name);
      }
    }
  }
  

  askQuestion(): void {
    if (!this.question.trim()) {
      alert('Veuillez entrer une question.');
      return;
    }

    if (!this.file) {
      alert('Veuillez télécharger un fichier PDF.');
      return;
    }

    this.loading = true;

    this.apiService.askQuestion(this.file, this.question).subscribe({
      next: (response) => {
        this.answer = response.answer;
        this.messages.push({ content: this.question, sender: 'user' });
        this.messages.push({ content: this.answer, sender: 'bot' });
      },
      error: (error) => {
        alert(`Erreur du serveur : ${error.error?.detail || 'Une erreur est survenue'}`);
      },
      complete: () => {
        this.loading = false;
      },
    });
  }
}
