#
# Conditional build:
%bcond_with	doc	# build docs (broken)
#
%include	/usr/lib/rpm/macros.java
Summary:	Open source implementation of JMX Java API
Summary(pl.UTF-8):	Implementacja API Javy JMX z otwartymi źródłami
Name:		mx4j
Version:	3.0.2
Release:	0.2
Epoch:		0
License:	Apache License
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/mx4j/%{name}-%{version}-src.tar.gz
# Source0-md5:	1c01f620c21efb0a84c3105c064b9047
URL:		http://mx4j.sourceforge.net/
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	axis
BuildRequires:	jaf
BuildRequires:	jakarta-bcel >= 5.0
BuildRequires:	jakarta-commons-logging >= 1.0.1
BuildRequires:	javamail >= 1.2
BuildRequires:	jce >= 1.2.2
BuildRequires:	jpackage-utils
BuildRequires:	jsse >= 1.0.2
BuildRequires:	rpm-javaprov
BuildRequires:	junit >= 3.8
BuildRequires:	jython >= 2.1
BuildRequires:	logging-log4j >= 1.2.7
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xml-commons
Requires:	jre
Provides:	jmxri
Obsoletes:	openjmx
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenJMX is an open source implementation of the Java(TM) Management
Extensions (JMX).

%description -l pl.UTF-8
OpenJMX to implementacja standardu JMX (Java(TM) Management
Extensions) z otwartymi źródłami.

%package doc
Summary:	Manual for %{name}
Summary(fr.UTF-8):	Documentation pour %{name}
Summary(it.UTF-8):	Documentazione di %{name}
Summary(pl.UTF-8):	Podręcznik dla %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l pl.UTF-8
Dokumentacja do %{name}.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc do %{name}.

%prep
%setup -q

%build
required_jars="\
activation \
mailapi.jar \
javamail/smtp \
jython \
commons-logging \
xml-commons-apis \
bcel \
jsse \
jce \
log4j \
junit \
jaxp_transform_impl \
"

export CLASSPATH=$(build-classpath $required_jars)

#ln -sf %{_javalibdir}/commons-logging.jar lib/
#ln -sf %{_javalibdir}/mail.jar lib/
#ln -sf %{_javalibdir}/activation.jar lib/
#ln -sf %{_javalibdir}/jython.jar lib/
#ln -sf %{_javalibdir}/log4j.jar lib/
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-jmx-module.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-mx4j-module.jar

cd build
%ant main %{?with_docs:javadocs docs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/lib/%{name}-actions.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-actions-%{version}.jar
cp -a dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-jmx-%{version}.jar
cp -a dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tools-%{version}.jar
ln -sf %{name}-actions-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-actions.jar
ln -sf %{name}-jmx-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-jmx.jar
ln -sf %{name}-tools-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tools.jar

# javadoc
%if %{with doc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with doc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
