import { Component, OnInit } from '@angular/core';
import { CoreService } from '../../core/core.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  topOffers: any;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    window.addEventListener('scroll', this.changeStyleOnScroll, true);
    this.getTopOffers();
  }

  getTopOffers() {
    this.coreService.getTopList().subscribe(
      data => { this.topOffers = data; },
      error => { console.log(error.message); }
    );
  }

  changeStyleOnScroll() {
    const scrollPercent = document.scrollingElement.scrollTop / 410;

    const h1 = document.getElementById('scroll-me');
    const translateValue = -1 * Math.max(Math.round((1 - scrollPercent) * 110), 0);
    const color = Math.min(Math.max(Math.round((1 - scrollPercent) * 100), 63), 100);
    h1.style.color = 'hsl(358, 100%,' + color + '%)';
    h1.style.transform = 'translateY(' + String(translateValue) + 'px)';

    const fa = document.getElementById('fa');
    const iconSize = Math.round((1 - scrollPercent) * 24);
    fa.style.fontSize = String(iconSize) + 'px';
  }
}
