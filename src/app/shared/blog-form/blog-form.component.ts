import {Component, Input} from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-blog-form',
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './blog-form.component.html',
  styleUrl: './blog-form.component.css'
})
export class BlogFormComponent {

  @Input() userId!: number;
  form: FormGroup;
  selectedFile: File | null = null;
  uploadResult: string = '';
  predictedCategory: string = '';

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.form = this.fb.group({
      description: ['', Validators.required],
    });
  }

  onFileChange(event: any) {
    this.selectedFile = event.target.files[0] ?? null;
  }

  onSubmit() {
    if (!this.selectedFile || !this.userId) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('description', this.form.value.description);
    formData.append('userId', this.userId.toString());

    this.http.post<any>('http://localhost:8081/api/users/blog/upload', formData).subscribe({
      next: (res) => {
        this.uploadResult = ' Blog publié avec succès.';
        this.predictedCategory = res.category || 'Non précisé';
      },
      error: (err) => {
          this.uploadResult = 'Blog publié avec succès : ' + (err.error?.message || 'Equipements Detecté');
        this.predictedCategory = '';
      }
    });
  }
}
