import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/core/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  showErrorMessage = false;

  constructor(
    protected formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  ngOnInit() {
    if (this.authService.currentUserValue) {
      this.router.navigate(['/admin']);
    }
  }

  submit() {
    if (this.loginForm.invalid) {
      this.showErrorMessage = true;

      return;
    } else {
      this.authService
        .login(this.loginForm.value.username, this.loginForm.value.password)
        .then(() => {
          this.router.navigateByUrl('admin');
        });
    }
  }
}
