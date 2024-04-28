#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Mail
%define		pnam	DMARC
Summary:	Mail::DMARC - Perl implementation of DMARC
Name:		perl-Mail-DMARC
Version:	1.20240314
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Mail/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	ecd5055af5262b65872b47ab86956fb9
URL:		https://metacpan.org/release/Mail-DMARC
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	perl(DBIx::Simple) >= 1.35
BuildRequires:	perl(Net::IDN::Encode)
BuildRequires:	perl(Test::File::ShareDir)
BuildRequires:	perl(XML::LibXML)
BuildRequires:	perl-Config-Tiny
BuildRequires:	perl-DBD-SQLite >= 1.31
BuildRequires:	perl-Email-MIME
BuildRequires:	perl-Email-Sender >= 1.300032
BuildRequires:	perl-Email-Simple
BuildRequires:	perl-File-Copy-Recursive
BuildRequires:	perl-File-ShareDir >= 1.00
BuildRequires:	perl-IO-Socket-SSL
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-DNS-Resolver-Mock
BuildRequires:	perl-Net-IP
BuildRequires:	perl-Net-SSLeay
BuildRequires:	perl-Regexp-Common >= 2013031301
BuildRequires:	perl-Socket6 >= 0.23
BuildRequires:	perl-Test-Exception
BuildRequires:	perl-Test-Output
BuildRequires:	perl-URI
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module is a suite of tools for implementing DMARC. It adheres to
the 2013 DMARC draft, intending to implement every MUST and every
SHOULD.

This module can be used by...

When a message arrives via SMTP, the MTA or filtering application can
pass in a small amount of metadata about the connection (envelope
details, SPF and DKIM results) to Mail::DMARC. When the validate
method is called, Mail::DMARC will determine if:

a. the header_from domain exists b. the header_from domain publishes a
DMARC policy c. if a policy is published... d. does the message
conform to the published policy? e. did the policy request reporting?
If so, save details.

The validation results are returned as a Mail::DMARC::Result object.
If the author domain requested a report, it was saved to the Report
Store. The Store class includes a SQL implementation that is tested
with SQLite, MySQL and PostgreSQL.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Build.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a example $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -rf dmarc-docs
mv $RPM_BUILD_ROOT%{perl_vendorlib}/auto/share/dist/Mail-DMARC dmarc-docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dmarc-docs/*
%attr(755,root,root) %{_bindir}/dmarc_http_client
%attr(755,root,root) %{_bindir}/dmarc_httpd
%attr(755,root,root) %{_bindir}/dmarc_lookup
%attr(755,root,root) %{_bindir}/dmarc_receive
%attr(755,root,root) %{_bindir}/dmarc_send_reports
%attr(755,root,root) %{_bindir}/dmarc_update_public_suffix_list
%attr(755,root,root) %{_bindir}/dmarc_view_reports
%{perl_vendorlib}/Mail/*.pm
%{perl_vendorlib}/Mail/DMARC
%{_mandir}/man1/dmarc*.1*
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
