import { Component, OnInit } from '@angular/core';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { CoreService } from '../../core/core.service';
import { Offer } from '../../core/VO/Offer';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss'],
  animations: [
    trigger('expand', [
      state('collapsed', style({ height: '65px' })),
      state('expanded', style({ height: '380px' })),
      transition('collapsed <=> expanded', [animate('0.3s')])
    ])
  ]
})
export class AdminPanelComponent implements OnInit {
  newOffer = new Offer('', '', '');
  offers: any;
  maxPage = 0;
  currentPage = 0;
  expand = [];
  add = false;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.getNumberOfOffers();
  }

  getNumberOfOffers() {
    console.log('interested?');
    this.coreService.getNumberOfOffers().subscribe(
      data => {
        this.maxPage = Math.ceil(JSON.parse(JSON.stringify(data)).count / 5);
      },
      error => {
        console.log(error.message);
      }
    );

    this.getOffers(0);
  }

  getOffers(pageNo) {
    this.currentPage = pageNo;
    this.coreService.getOffersByPage(pageNo, 5).subscribe(
      data => {
        this.offers = data;
        for (let i = 0; i < this.offers.length; i++) {
          this.expand[i] = false;
        }
      },
      error => {
        console.log(error.message);
      }
    );
  }

  expandForm(j) {
    for (let i = 0; i < this.offers.length; i++) {
      this.expand[i] = i === j;
    }
  }

  delete(j) {
    this.coreService.deleteOffer(this.offers[j].id).subscribe(
      data => {
        this.offers = data;
        this.expand = [];
        for (let i = 0; i < this.offers.length; i++) {
          this.expand[i] = false;
        }
        this.getNumberOfOffers();
      },
      error => {
        console.log(error.message);
      }
    );
  }
}
