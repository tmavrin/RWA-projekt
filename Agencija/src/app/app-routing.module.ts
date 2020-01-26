import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContactComponent } from './contact/contact.component';
import { OfferComponent } from './offer/offer.component';
import { LoginComponent } from './login/login.component';
import { TestApiComponent } from './test-api/test-api.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'offer', component: OfferComponent },
  { path: 'login', component: LoginComponent},
  { path: 'test-api', component: TestApiComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
