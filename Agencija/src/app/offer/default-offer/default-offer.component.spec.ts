import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DefaultOfferComponent } from './default-offer.component';

describe('DefaultOfferComponent', () => {
  let component: DefaultOfferComponent;
  let fixture: ComponentFixture<DefaultOfferComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DefaultOfferComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DefaultOfferComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
