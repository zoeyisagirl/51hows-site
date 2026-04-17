import zh from './zh';
import en from './en';

export type Locale = 'zh' | 'en';
export type Translations = typeof zh;

const dictionaries: Record<Locale, Translations> = { zh, en };

export function getDictionary(locale: Locale): Translations {
  return dictionaries[locale] ?? dictionaries.zh;
}

export function getLocaleFromUrl(url: URL): Locale {
  const [, locale] = url.pathname.split('/');
  if (locale === 'en') return 'en';
  return 'zh'; // default
}
